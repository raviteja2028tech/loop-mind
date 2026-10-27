"""Tests for Recruitment Outcome & Closed-Loop Intelligence — phase.md
Phase 16.

Two things matter here: (1) an outcome can only be recorded once the
interview has actually happened ("completed"), and (2) both directions of
the closed loop are real — a "hired" outcome contributes a genuine,
recruiter-isolated historical signal to future candidates for the same job
role (`test_hired_outcome_contributes_historical_signal_to_future_candidate`
and `test_historical_signal_never_leaks_across_recruiters`), and a
"not_selected" outcome surfaces the same skill-gap reason to the student
that disapproval already does (`test_not_selected_outcome_reaches_student`).
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


def _apply_with_skills(client, student_headers, job_id, skills, full_name="Demo Candidate"):
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": full_name,
            "date_of_birth": "2003-03-03",
            "gender": "female",
            "email": f"{full_name.replace(' ', '.').lower()}@example.com",
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


def _make_job(client, recruiter_headers, skills, job_role="Backend Developer"):
    return client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": job_role,
            "experience_required": "Entry Level",
            "required_skills": skills,
        },
        headers=recruiter_headers,
    ).json()


def _take_to_completed(client, recruiter_headers, application_id):
    client.post(
        f"/api/recruiters/me/candidates/{application_id}/approve", headers=recruiter_headers
    )
    client.post(
        f"/api/recruiters/me/interviews/{application_id}/schedule",
        json={"interview_type": "Technical", "scheduled_at": "2026-10-01T10:00:00Z"},
        headers=recruiter_headers,
    )
    client.put(
        f"/api/recruiters/me/interviews/{application_id}/status",
        json={"status": "completed"},
        headers=recruiter_headers,
    )


def test_outcome_requires_completed_interview(client):
    _add_recruiter(client, "9812470001")
    recruiter_headers = _login(client, "9812470001")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812470002")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    # Not even approved yet.
    res = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "hired"},
        headers=recruiter_headers,
    )
    assert res.status_code == 400

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    # Approved but not scheduled/completed yet.
    res = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "hired"},
        headers=recruiter_headers,
    )
    assert res.status_code == 400


def test_hired_outcome_recorded_and_reaches_student(client):
    _add_recruiter(client, "9812470003")
    recruiter_headers = _login(client, "9812470003")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812470004")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])
    _take_to_completed(client, recruiter_headers, application["id"])

    res = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "hired"},
        headers=recruiter_headers,
    )
    assert res.status_code == 200
    detail = res.json()
    assert detail["outcome"] == "hired"
    assert detail["outcome_label"] == "Hired"
    # Interview Status stays "Completed" — outcome is a separate axis, never merged.
    assert detail["status_label"] == "Completed"

    my_apps = client.get("/api/students/me/jobs/applications", headers=student_headers).json()
    assert my_apps[0]["status_label"] == "Hired"


def test_not_selected_outcome_reaches_student(client):
    _add_recruiter(client, "9812470005")
    recruiter_headers = _login(client, "9812470005")
    job = _make_job(client, recruiter_headers, ["Python", "System Design"])
    student_headers = _register_student(client, "9812470006")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])
    _take_to_completed(client, recruiter_headers, application["id"])

    res = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "not_selected", "reason": "Skill Gap: System Design"},
        headers=recruiter_headers,
    )
    assert res.status_code == 200
    detail = res.json()
    assert detail["outcome_label"] == "Not Selected"
    assert detail["outcome_reason"] == "Skill Gap: System Design"

    my_apps = client.get("/api/students/me/jobs/applications", headers=student_headers).json()
    assert my_apps[0]["status_label"] == "Not Selected"
    assert my_apps[0]["disapproval_reason"] == "Skill Gap: System Design"


def test_hired_outcome_contributes_historical_signal_to_future_candidate(client):
    _add_recruiter(client, "9812470007")
    recruiter_headers = _login(client, "9812470007")
    job = _make_job(client, recruiter_headers, ["Python", "SQL"], job_role="Data Engineer")

    # First candidate: strong match, gets hired.
    first_headers = _register_student(client, "9812470008")
    first_app = _apply_with_skills(
        client, first_headers, job["id"], ["Python", "SQL"], full_name="First Candidate"
    )
    _take_to_completed(client, recruiter_headers, first_app["id"])
    client.put(
        f"/api/recruiters/me/interviews/{first_app['id']}/outcome",
        json={"outcome": "hired"},
        headers=recruiter_headers,
    )

    # Second job, same role, second candidate shares skills with the hire.
    job2 = _make_job(client, recruiter_headers, ["Python", "SQL"], job_role="Data Engineer")
    second_headers = _register_student(client, "9812470009")
    second_app = _apply_with_skills(
        client, second_headers, job2["id"], ["Python", "SQL"], full_name="Second Candidate"
    )

    workflow = client.get(
        f"/api/recruiters/me/candidates/{second_app['id']}/workflow", headers=recruiter_headers
    ).json()
    assert workflow["historical_signal"] is not None
    assert "Data Engineer" in workflow["historical_signal"]


def test_historical_signal_never_leaks_across_recruiters(client):
    _add_recruiter(client, "9812470010")
    _add_recruiter(client, "9812470011")
    headers_a = _login(client, "9812470010")
    headers_b = _login(client, "9812470011")

    job_a = _make_job(client, headers_a, ["Python"], job_role="Data Engineer")
    student_a = _register_student(client, "9812470012")
    app_a = _apply_with_skills(client, student_a, job_a["id"], ["Python"], full_name="Candidate A")
    _take_to_completed(client, headers_a, app_a["id"])
    client.put(
        f"/api/recruiters/me/interviews/{app_a['id']}/outcome",
        json={"outcome": "hired"},
        headers=headers_a,
    )

    # Recruiter B posts the *same* job role independently — must not see A's hire signal.
    job_b = _make_job(client, headers_b, ["Python"], job_role="Data Engineer")
    student_b = _register_student(client, "9812470013")
    app_b = _apply_with_skills(client, student_b, job_b["id"], ["Python"], full_name="Candidate B")

    workflow = client.get(
        f"/api/recruiters/me/candidates/{app_b['id']}/workflow", headers=headers_b
    ).json()
    assert workflow["historical_signal"] is None


def test_outcome_requires_recruiter_role_and_ownership(client):
    _add_recruiter(client, "9812470014")
    _add_recruiter(client, "9812470015")
    headers_a = _login(client, "9812470014")
    headers_b = _login(client, "9812470015")

    job = _make_job(client, headers_a, ["Python"])
    student_headers = _register_student(client, "9812470016")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])
    _take_to_completed(client, headers_a, application["id"])

    res = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "hired"},
        headers=headers_b,
    )
    assert res.status_code == 404

    res = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "hired"},
        headers=student_headers,
    )
    assert res.status_code == 403
