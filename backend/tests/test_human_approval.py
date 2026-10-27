"""Tests for Human Approval & Recruitment Outcome — phase.md Phase 14.

The critical requirement here is the separation spec.md demands: "AI
Status: Rejected / Human Decision: Approved ... must remain technically
distinguishable" — these tests specifically exercise a case where the
human decision disagrees with the AI status, proving one never silently
overwrites the other.
"""

import io

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


def _apply_with_skills(client, student_headers, job_id, skills):
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
    for skill in skills:
        client.post(
            "/api/students/me/skills",
            json={
                "skill_name": skill,
                "skill_category": "General",
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
    res = client.post(f"/api/students/me/jobs/{job_id}/apply", headers=student_headers)
    assert res.status_code == 200
    return res.json()


def test_approve_sets_human_decision_and_shortlists_the_bucket(client):
    _add_recruiter(client, "9812450001")
    recruiter_headers = _login(client, "9812450001")

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
    student_headers = _register_student(client, "9812450002")
    application = _apply_with_skills(client, student_headers, job["id"], [])  # weak match

    res = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    assert res.status_code == 200
    body = res.json()
    assert body["human_decision"] == "approved"
    stage_states = {s["key"]: s["state"] for s in body["stages"]}
    assert stage_states["human_approval"] == "approved"

    candidates = client.get("/api/recruiters/me/candidates", headers=recruiter_headers).json()
    row = candidates["candidates"][0]
    assert row["status_label"] == "Shortlisted"  # human override
    assert candidates["summary"]["shortlisted"] == 1


def test_disapprove_records_reason_and_overrides_ai_status_distinctly(client):
    _add_recruiter(client, "9812450003")
    recruiter_headers = _login(client, "9812450003")

    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
            "required_skills": ["Python", "SQL"],
        },
        headers=recruiter_headers,
    ).json()
    student_headers = _register_student(client, "9812450004")
    # Strong skill match -> AI should shortlist this candidate.
    application = _apply_with_skills(client, student_headers, job["id"], ["Python", "SQL"])

    pre = client.get("/api/recruiters/me/candidates", headers=recruiter_headers).json()
    assert pre["candidates"][0]["ai_evaluation_label"] == "Shortlisted"

    res = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/disapprove",
        json={"reason": "Skill Gap: System Design"},
        headers=recruiter_headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["human_decision"] == "disapproved"
    assert body["disapproval_reason"] == "Skill Gap: System Design"
    stage_states = {s["key"]: s["state"] for s in body["stages"]}
    assert stage_states["human_approval"] == "rejected"

    # The critical separation: AI status stays Shortlisted (untouched),
    # while the overall bucket/status_label reflects the human override.
    post = client.get("/api/recruiters/me/candidates", headers=recruiter_headers).json()
    row = post["candidates"][0]
    assert row["ai_evaluation_label"] == "Shortlisted"
    assert row["status_label"] == "Rejected"
    assert post["summary"]["rejected"] == 1
    assert post["summary"]["shortlisted"] == 0

    # Student-side: the disapproval and its specific reason are visible
    # through the existing Jobs-page "My Applications" access point.
    my_apps = client.get("/api/students/me/jobs/applications", headers=student_headers).json()
    assert my_apps[0]["status_label"] == "Disapproved"
    assert my_apps[0]["disapproval_reason"] == "Skill Gap: System Design"


def test_recruiter_can_change_an_earlier_decision(client):
    _add_recruiter(client, "9812450005")
    recruiter_headers = _login(client, "9812450005")

    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
        },
        headers=recruiter_headers,
    ).json()
    student_headers = _register_student(client, "9812450006")
    application = _apply_with_skills(client, student_headers, job["id"], [])

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/disapprove",
        json={"reason": "Not a fit"},
        headers=recruiter_headers,
    )
    res = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    body = res.json()
    assert body["human_decision"] == "approved"
    assert body["disapproval_reason"] is None  # cleared on re-approval


def test_approve_requires_ownership(client):
    _add_recruiter(client, "9812450007")
    _add_recruiter(client, "9812450008")
    headers_a = _login(client, "9812450007")
    headers_b = _login(client, "9812450008")

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
    student_headers = _register_student(client, "9812450009")
    application = _apply_with_skills(client, student_headers, job["id"], [])

    res = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=headers_b
    )
    assert res.status_code == 404


def test_approve_requires_recruiter_role(client):
    headers = _register_student(client, "9812450010")
    res = client.post("/api/recruiters/me/candidates/1/approve", headers=headers)
    assert res.status_code == 403
