"""Tests for Recruitment Analytics & Historical Intelligence — phase.md
Phase 17.

spec.md's "Dynamic rule" for this page is explicit: "All statistics and
charts derive from stored project data. No permanent screenshot values."
These tests exercise that every number changes in response to real stored
outcomes (a hire moves the funnel and the successful-candidate profile; a
skill gap shows up in skill_gap_trends) and that recruiter isolation holds.
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


def test_analytics_empty_for_a_fresh_recruiter(client):
    _add_recruiter(client, "9812480001")
    recruiter_headers = _login(client, "9812480001")

    res = client.get("/api/recruiters/me/analytics", headers=recruiter_headers)
    assert res.status_code == 200
    body = res.json()
    assert all(stage["count"] == 0 for stage in body["funnel"])
    assert body["outcomes"] == []
    assert body["skill_trends"] == []
    assert body["successful_candidate_profile"]["total_hired"] == 0


def test_analytics_reflects_real_hire_and_skill_gap(client):
    _add_recruiter(client, "9812480002")
    recruiter_headers = _login(client, "9812480002")
    job = _make_job(client, recruiter_headers, ["Python", "SQL"], job_role="Data Analyst")
    student_headers = _register_student(client, "9812480003")
    application = _apply_with_skills(
        client, student_headers, job["id"], ["Python"], full_name="Analytics Candidate"
    )

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    client.post(
        f"/api/recruiters/me/interviews/{application['id']}/schedule",
        json={"interview_type": "Technical", "scheduled_at": "2026-10-01T10:00:00Z"},
        headers=recruiter_headers,
    )
    client.put(
        f"/api/recruiters/me/interviews/{application['id']}/status",
        json={"status": "completed"},
        headers=recruiter_headers,
    )
    client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "hired"},
        headers=recruiter_headers,
    )

    res = client.get("/api/recruiters/me/analytics", headers=recruiter_headers)
    body = res.json()

    funnel = {stage["label"]: stage["count"] for stage in body["funnel"]}
    assert funnel["Applied"] == 1
    assert funnel["Hired"] == 1

    outcome_labels = {slice_["label"] for slice_ in body["outcomes"]}
    assert "Hired" in outcome_labels

    skill_trend_names = {t["skill"] for t in body["skill_trends"]}
    assert "python" in skill_trend_names

    gap_trend_names = {t["skill"] for t in body["skill_gap_trends"]}
    assert "sql" in gap_trend_names

    profile = body["successful_candidate_profile"]
    assert profile["total_hired"] == 1
    assert "python" in profile["top_skills"]

    patterns = body["company_patterns"]
    assert len(patterns) == 1
    assert patterns[0]["job_id"] == job["id"]
    assert patterns[0]["applications"] == 1
    assert patterns[0]["hire_rate_percentage"] == 100

    assert len(body["stage_trends"]) >= 1
    assert sum(p["applications"] for p in body["stage_trends"]) == 1


def test_analytics_isolated_per_recruiter(client):
    _add_recruiter(client, "9812480004")
    _add_recruiter(client, "9812480005")
    headers_a = _login(client, "9812480004")
    headers_b = _login(client, "9812480005")

    job_a = _make_job(client, headers_a, ["Python"])
    student_a = _register_student(client, "9812480006")
    _apply_with_skills(client, student_a, job_a["id"], ["Python"], full_name="Candidate A")

    res_b = client.get("/api/recruiters/me/analytics", headers=headers_b)
    body_b = res_b.json()
    assert all(stage["count"] == 0 for stage in body_b["funnel"])
    assert body_b["company_patterns"] == []


def test_analytics_requires_recruiter_role(client):
    headers = _register_student(client, "9812480007")
    res = client.get("/api/recruiters/me/analytics", headers=headers)
    assert res.status_code == 403
