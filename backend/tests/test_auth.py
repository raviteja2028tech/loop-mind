import pytest
from fastapi import HTTPException

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.seed import DEMO_RECRUITER_MOBILE, DEMO_STUDENT_MOBILE
from backend.tests.conftest import complete_registration

NEW_STUDENT_MOBILE = "9876543210"


def test_register_new_student_full_flow(client):
    # Registering a brand-new mobile number sends an OTP.
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": NEW_STUDENT_MOBILE, "purpose": "register"}
    )
    assert res.status_code == 200
    otp = res.json()["dev_otp"]
    assert otp is not None and len(otp) == 4

    # Wrong OTP is rejected with the exact spec'd message.
    wrong = "0000" if otp != "0000" else "1111"
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": NEW_STUDENT_MOBILE, "code": wrong, "purpose": "register"},
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Incorrect OTP, please try again"

    # Student Create Account UPDATE SDD §1/§3/§12: correct OTP issues only
    # a registration-draft token — no permanent account exists yet.
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": NEW_STUDENT_MOBILE, "code": otp, "purpose": "register"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["role"] == "registration"
    assert body["redirect"] == "/app"

    # The issued token identifies the draft, not a student, on /me.
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {body['token']}"})
    assert res.status_code == 200
    me = res.json()
    assert me["mobile_number"] == NEW_STUDENT_MOBILE
    assert me["role"] == "registration"

    # The registration-draft token cannot reach real student endpoints.
    res = client.get(
        "/api/students/me/basic-info", headers={"Authorization": f"Bearer {body['token']}"}
    )
    assert res.status_code == 403

    # Only completing Basic Information + consent through Create Account
    # produces a real student account.
    real_token = complete_registration(client, NEW_STUDENT_MOBILE, body["token"])
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {real_token}"})
    assert res.status_code == 200
    assert res.json()["role"] == "student"


def _register_and_create_account(client, mobile: str) -> str:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "register"}
    )
    return complete_registration(client, mobile, res.json()["token"])


def test_register_existing_mobile_rejected(client):
    _register_and_create_account(client, NEW_STUDENT_MOBILE)
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": NEW_STUDENT_MOBILE, "purpose": "register"}
    )
    assert res.status_code == 409
    assert "already been created" in res.json()["detail"]


def test_login_unknown_mobile_rejected(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "1111111111", "purpose": "login"}
    )
    assert res.status_code == 404
    assert "No account exists" in res.json()["detail"]


def test_login_existing_student_succeeds(client):
    _register_and_create_account(client, NEW_STUDENT_MOBILE)
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": NEW_STUDENT_MOBILE, "purpose": "login"}
    )
    assert res.status_code == 200
    otp = res.json()["dev_otp"]

    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": NEW_STUDENT_MOBILE, "code": otp, "purpose": "login"},
    )
    assert res.status_code == 200
    assert res.json()["role"] == "student"
    assert res.json()["redirect"] == "/app"


def test_login_demo_recruiter_routes_to_recruiter_portal(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": DEMO_RECRUITER_MOBILE, "purpose": "login"}
    )
    assert res.status_code == 200
    otp = res.json()["dev_otp"]

    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": DEMO_RECRUITER_MOBILE, "code": otp, "purpose": "login"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["role"] == "recruiter"
    assert body["redirect"] == "/recruiter"


def test_dev_otp_is_always_the_fixed_demo_code(client):
    """User-requested demo convenience: in dev mode the OTP is always the
    same fixed code (never random), so a demo never requires reading the
    API response to find it."""
    from backend.core.security import DEV_OTP_CODE

    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9123450001", "purpose": "register"}
    )
    assert res.json()["dev_otp"] == DEV_OTP_CODE

    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9123450002", "purpose": "register"}
    )
    assert res.json()["dev_otp"] == DEV_OTP_CODE


def test_login_demo_student_routes_to_student_portal(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": DEMO_STUDENT_MOBILE, "purpose": "login"}
    )
    assert res.status_code == 200
    otp = res.json()["dev_otp"]

    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": DEMO_STUDENT_MOBILE, "code": otp, "purpose": "login"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["role"] == "student"
    assert body["redirect"] == "/app"


def test_resend_before_cooldown_is_rejected(client):
    mobile = "9123456780"
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    assert res.status_code == 200

    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    assert res.status_code == 429


def test_role_separation_recruiter_fails_student_only_dependency():
    """spec.md "Critical rule": a recruiter must not receive Student Portal
    functionality. Dedicated student/recruiter-only endpoints (Phase 05/11)
    depend on `require_role`; exercised directly here without going
    through the full HTTP stack."""
    recruiter_account = CurrentAccount(
        account_id=1, role="recruiter", mobile_number=DEMO_RECRUITER_MOBILE
    )
    student_only = require_role("student")

    with pytest.raises(HTTPException) as exc_info:
        student_only(recruiter_account)
    assert exc_info.value.status_code == 403


def test_invalid_mobile_number_rejected_by_schema(client):
    res = client.post("/api/auth/send-otp", json={"mobile_number": "12345", "purpose": "login"})
    assert res.status_code == 422
