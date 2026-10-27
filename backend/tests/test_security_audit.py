"""Security & Authorization Audit — phase.md Phase 21.

This is an audit phase, not a feature phase: these tests verify the
implementation against spec.md's own authorization/data-isolation
requirements rather than introducing new, unspecified security machinery.

- Portal isolation: a student token must be rejected by every
  recruiter-only endpoint and vice versa (spec.md "Student cannot access
  Recruiter functionality. Recruiter cannot access Student functionality
  outside defined shared flows.").
- Data isolation / IDOR: a recruiter must never reach another recruiter's
  job/candidate/interview records, and a student must never reach another
  student's skill/application records, by ID alone.
- Authentication integrity: a tampered or malformed JWT must be rejected,
  not silently accepted.
- AI/human boundary: approval is the only way a candidate's human-facing
  decision is recorded; the AI's own status is never silently promoted
  into one (already exercised in depth by test_human_approval.py — the
  assertion here is the narrower "no approval record exists until the
  recruiter acts" check).
"""

import io

import jwt

from backend.core.config import PROFILE_PHOTOS_DIR, settings
from backend.models.recruiter import Recruiter
from backend.tests.conftest import complete_registration


def _register_student(client, mobile: str) -> dict:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "register"}
    )
    token = complete_registration(client, mobile, res.json()["token"])
    return {"Authorization": f"Bearer {token}"}


def _login(client, mobile: str) -> dict:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "login"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "login"}
    )
    return {"Authorization": f"Bearer {res.json()['token']}"}


def _db(client):
    from backend.core.database import get_db
    from backend.main import app

    return next(app.dependency_overrides[get_db]())


def _add_recruiter(client, mobile: str) -> None:
    db = _db(client)
    db.add(Recruiter(mobile_number=mobile, name="Fresh Recruiter"))
    db.commit()


# ---- Portal isolation ----

_RECRUITER_ONLY_ENDPOINTS = [
    ("get", "/recruiters/me/dashboard"),
    ("get", "/recruiters/me/jobs"),
    ("post", "/recruiters/me/jobs"),
    ("get", "/recruiters/me/candidates"),
    ("get", "/recruiters/me/interviews"),
    ("get", "/recruiters/me/analytics"),
]

_STUDENT_ONLY_ENDPOINTS = [
    ("get", "/students/me/dashboard"),
    ("get", "/students/me/basic-info"),
    ("get", "/students/me/skills"),
    ("get", "/students/me/jobs"),
    ("get", "/students/me/profile"),
    ("get", "/students/me/skill-gap"),
    ("get", "/students/me/preparation-plan-page"),
    ("delete", "/students/me/account"),
]


def test_student_token_rejected_by_every_recruiter_endpoint(client):
    headers = _register_student(client, "9812500001")
    for method, path in _RECRUITER_ONLY_ENDPOINTS:
        res = getattr(client, method)(f"/api{path}", headers=headers)
        assert res.status_code == 403, f"{method.upper()} {path} should reject a student token"


def test_recruiter_token_rejected_by_every_student_endpoint(client):
    _add_recruiter(client, "9812500002")
    headers = _login(client, "9812500002")
    for method, path in _STUDENT_ONLY_ENDPOINTS:
        res = getattr(client, method)(f"/api{path}", headers=headers)
        assert res.status_code == 403, f"{method.upper()} {path} should reject a recruiter token"


def test_unauthenticated_requests_rejected(client):
    for method, path in _RECRUITER_ONLY_ENDPOINTS + _STUDENT_ONLY_ENDPOINTS:
        res = getattr(client, method)(f"/api{path}")
        assert res.status_code in (401, 403), (
            f"{method.upper()} {path} should require authentication"
        )


# ---- Data isolation / IDOR ----


def test_recruiter_cannot_reach_another_recruiters_job_by_id(client):
    _add_recruiter(client, "9812500003")
    _add_recruiter(client, "9812500004")
    headers_a = _login(client, "9812500003")
    headers_b = _login(client, "9812500004")

    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
        },
        headers=headers_a,
    ).json()

    res = client.get(f"/api/recruiters/me/jobs/{job['id']}", headers=headers_b)
    assert res.status_code == 404

    res = client.put(
        f"/api/recruiters/me/jobs/{job['id']}/status",
        json={"status": "paused"},
        headers=headers_b,
    )
    assert res.status_code == 404


def test_student_cannot_edit_or_delete_another_students_skill(client):
    headers_a = _register_student(client, "9812500005")
    headers_b = _register_student(client, "9812500006")

    skill = client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=headers_a,
    ).json()

    res = client.put(
        f"/api/students/me/skills/{skill['id']}",
        json={
            "skill_name": "Hacked",
            "skill_category": "Programming",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=headers_b,
    )
    assert res.status_code == 404

    res = client.delete(f"/api/students/me/skills/{skill['id']}", headers=headers_b)
    assert res.status_code == 404

    # Untouched — still present, still the original values.
    skills_a = client.get("/api/students/me/skills", headers=headers_a).json()
    assert len(skills_a) == 1
    assert skills_a[0]["skill_name"] == "Python"


def test_student_profile_endpoints_never_mix_data_across_students(client):
    headers_a = _register_student(client, "9812500007")
    headers_b = _register_student(client, "9812500008")

    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Student A",
            "date_of_birth": "2003-01-01",
            "gender": "female",
            "email": "a@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=headers_a,
    )

    # Student Create Account UPDATE SDD: B's account already has its own
    # (placeholder) Basic Information from registration — the isolation
    # property under test is that it's B's own data, never A's.
    profile_b = client.get("/api/students/me/profile", headers=headers_b).json()
    assert profile_b["overview"]["full_name"] == "Test Student"

    basic_b = client.get("/api/students/me/basic-info", headers=headers_b)
    assert basic_b.json()["full_name"] == "Test Student"


def test_recruiter_cannot_reach_another_recruiters_candidate_workflow(client):
    _add_recruiter(client, "9812500009")
    _add_recruiter(client, "9812500010")
    headers_a = _login(client, "9812500009")
    headers_b = _login(client, "9812500010")

    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
        },
        headers=headers_a,
    ).json()
    student_headers = _register_student(client, "9812500011")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Candidate",
            "date_of_birth": "2003-01-01",
            "gender": "male",
            "email": "c@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=student_headers,
    )
    client.post(
        "/api/students/me/resume",
        headers=student_headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    application = client.post(
        f"/api/students/me/jobs/{job['id']}/apply", headers=student_headers
    ).json()

    res = client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=headers_b
    )
    assert res.status_code == 404
    res = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=headers_b
    )
    assert res.status_code == 404


# ---- File upload safety ----


def test_profile_photo_upload_rejects_path_traversal_in_filename(client):
    """A crafted filename extension (e.g. "x.png/../../evil") must never
    let an uploaded file land outside PROFILE_PHOTOS_DIR — the extension
    is derived from client-controlled input, so it must be sanitized
    rather than trusted (phase.md Phase 21 audit finding, fixed in
    backend/routes/students.py's upload_profile_photo)."""
    headers = _register_student(client, "9812500015")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Traversal Test",
            "date_of_birth": "2003-01-01",
            "gender": "male",
            "email": "trav@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=headers,
    )

    malicious_name = "x.png/../../../evil"
    res = client.post(
        "/api/students/me/basic-info/photo",
        headers=headers,
        files={"file": (malicious_name, io.BytesIO(b"\x89PNG fake"), "image/png")},
    )
    assert res.status_code == 200
    stored_path = res.json()["profile_photo_path"]

    # The stored path must resolve inside PROFILE_PHOTOS_DIR, not escape it.
    from pathlib import Path

    resolved = Path(stored_path).resolve()
    assert resolved.parent == PROFILE_PHOTOS_DIR.resolve()
    # The traversal payload isn't a recognized extension, so it safely
    # falls back to a known-safe one rather than being used verbatim.
    assert resolved.suffix == ".jpg"
    resolved.unlink(missing_ok=True)


def test_profile_photo_upload_keeps_a_legitimate_extension(client):
    """The fix must not break the ordinary, honest case — a normal
    filename's real extension is preserved."""
    headers = _register_student(client, "9812500016")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Normal Upload",
            "date_of_birth": "2003-01-01",
            "gender": "female",
            "email": "normal@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=headers,
    )
    res = client.post(
        "/api/students/me/basic-info/photo",
        headers=headers,
        files={"file": ("profile.png", io.BytesIO(b"\x89PNG fake"), "image/png")},
    )
    assert res.status_code == 200

    from pathlib import Path

    resolved = Path(res.json()["profile_photo_path"]).resolve()
    assert resolved.parent == PROFILE_PHOTOS_DIR.resolve()
    assert resolved.suffix == ".png"
    resolved.unlink(missing_ok=True)


# ---- Authentication integrity ----


def test_tampered_jwt_is_rejected(client):
    _add_recruiter(client, "9812500012")
    headers = _login(client, "9812500012")
    token = headers["Authorization"].split(" ")[1]
    tampered = token[:-4] + ("0000" if token[-4:] != "0000" else "1111")
    res = client.get(
        "/api/recruiters/me/dashboard", headers={"Authorization": f"Bearer {tampered}"}
    )
    assert res.status_code == 401


def test_jwt_signed_with_wrong_secret_is_rejected(client):
    forged = jwt.encode(
        {"sub": "1", "role": "recruiter", "mobile_number": "9999999999"},
        "not-the-real-secret",
        algorithm=settings.jwt_algorithm,
    )
    res = client.get("/api/recruiters/me/dashboard", headers={"Authorization": f"Bearer {forged}"})
    assert res.status_code == 401


def test_jwt_alg_none_is_rejected(client):
    """The classic "alg: none" forgery — decode_access_token must only
    ever accept the configured algorithm, never whatever the token claims."""
    forged = jwt.encode(
        {"sub": "1", "role": "recruiter", "mobile_number": "9999999999"},
        key=None,
        algorithm="none",
    )
    res = client.get("/api/recruiters/me/dashboard", headers={"Authorization": f"Bearer {forged}"})
    assert res.status_code == 401


def test_malformed_authorization_header_rejected(client):
    res = client.get("/api/recruiters/me/dashboard", headers={"Authorization": "Bearer not-a-jwt"})
    assert res.status_code == 401


# ---- AI / human boundary ----


def test_no_human_approval_exists_until_recruiter_explicitly_acts(client):
    _add_recruiter(client, "9812500013")
    recruiter_headers = _login(client, "9812500013")
    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
            "required_skills": ["Python"],
        },
        headers=recruiter_headers,
    ).json()
    student_headers = _register_student(client, "9812500014")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Candidate",
            "date_of_birth": "2003-01-01",
            "gender": "male",
            "email": "d@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=student_headers,
    )
    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=student_headers,
    )
    client.post(
        "/api/students/me/resume",
        headers=student_headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    application = client.post(
        f"/api/students/me/jobs/{job['id']}/apply", headers=student_headers
    ).json()

    # AI evaluation alone (even a strong match) must never appear to the
    # student as a final "Shortlisted" outcome — only a real HumanApproval
    # row can do that.
    workflow = client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=recruiter_headers
    ).json()
    assert workflow["human_decision"] is None

    my_apps = client.get("/api/students/me/jobs/applications", headers=student_headers).json()
    assert my_apps[0]["status_label"] == "Under Review"
