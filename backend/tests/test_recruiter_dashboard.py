"""Tests for the Recruiter Dashboard — phase.md Phase 11.

Job *creation* (Phase 12), AI matching (Phase 13) and human approval
(Phase 14) don't exist yet, so a freshly-registered recruiter with no
seeded data must see an honest all-zero dashboard, and every application
right now is "under review" with AI Status "Pending" — these tests lock
that in so a later phase's changes don't silently start fabricating
further-along statuses.
"""

from backend.core.seed_jobs import seed_jobs
from backend.models.recruiter import Recruiter
from backend.tests.conftest import complete_registration


def _login(client, mobile: str) -> dict:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "login"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "login"}
    )
    return {"Authorization": f"Bearer {res.json()['token']}"}


def _register_student(client, mobile: str) -> dict:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "register"}
    )
    token = complete_registration(client, mobile, res.json()["token"])
    return {"Authorization": f"Bearer {token}"}


def _db(client):
    from backend.core.database import get_db
    from backend.main import app

    return next(app.dependency_overrides[get_db]())


def _add_recruiter(client, mobile: str) -> None:
    db = _db(client)
    db.add(Recruiter(mobile_number=mobile, name="Fresh Recruiter"))
    db.commit()


def test_dashboard_is_honestly_empty_for_a_recruiter_with_no_jobs(client):
    _add_recruiter(client, "9812400001")
    headers = _login(client, "9812400001")

    res = client.get("/api/recruiters/me/dashboard", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["summary"] == {
        "total_jobs": 0,
        "total_applications": 0,
        "shortlisted": 0,
        "under_review": 0,
    }
    assert body["jobs"] == []
    assert body["pipeline"]["total"] == 0
    assert body["recent_applications"] == []
    assert body["upcoming_interviews"] == []
    assert body["recent_activity"] == []


def test_demo_recruiter_dashboard_reflects_seeded_jobs_and_real_applications(client):
    db = _db(client)
    seed_jobs(db)

    student_headers = _register_student(client, "9812400002")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Aditi Rao",
            "date_of_birth": "2003-03-03",
            "gender": "female",
            "email": "aditi@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=student_headers,
    )
    import io

    client.post(
        "/api/students/me/resume",
        headers=student_headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    apply_res = client.post("/api/students/me/jobs/1/apply", headers=student_headers)
    assert apply_res.status_code == 200

    recruiter_headers = _login(client, "9999999999")
    res = client.get("/api/recruiters/me/dashboard", headers=recruiter_headers)
    assert res.status_code == 200
    body = res.json()

    assert body["summary"]["total_jobs"] == 10
    assert body["summary"]["total_applications"] == 1
    assert body["summary"]["under_review"] == 1
    assert body["summary"]["shortlisted"] == 0

    job_1_row = next(j for j in body["jobs"] if j["id"] == 1)
    assert job_1_row["applications"] == 1
    assert job_1_row["under_review"] == 1
    assert job_1_row["status"] == "Active"

    assert body["pipeline"]["total"] == 1
    assert body["pipeline"]["under_review"]["count"] == 1
    assert body["pipeline"]["under_review"]["percentage"] == 100
    assert body["pipeline"]["rejected"]["count"] == 0

    assert len(body["recent_applications"]) == 1
    application = body["recent_applications"][0]
    assert application["candidate_name"] == "Aditi Rao"
    assert application["ai_status"] == "Pending"

    labels = [a["label"] for a in body["recent_activity"]]
    assert "New application received" in labels
    assert "Job created" in labels


def test_recruiter_dashboard_requires_recruiter_role(client):
    headers = _register_student(client, "9812400003")
    res = client.get("/api/recruiters/me/dashboard", headers=headers)
    assert res.status_code == 403
