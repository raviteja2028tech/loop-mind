"""Tests for Multi-Agent System 2 (AI Recruitment) — phase.md Phase 13.
Exercised through the Candidates page, its real entry point, rather than
calling the AI services directly, so these tests prove the full wiring
(DB -> service -> agents -> Qdrant -> DB) actually works end to end.
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


def _complete_profile_and_apply(client, student_headers, job_id, skills):
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


def test_strong_match_candidate_gets_high_score_and_shortlisted(client):
    _add_recruiter(client, "9812430001")
    recruiter_headers = _login(client, "9812430001")

    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
            "required_skills": ["Python", "SQL", "Django"],
        },
        headers=recruiter_headers,
    ).json()

    student_headers = _register_student(client, "9812430002")
    _complete_profile_and_apply(client, student_headers, job["id"], ["Python", "SQL", "Django"])

    res = client.get("/api/recruiters/me/candidates", headers=recruiter_headers)
    assert res.status_code == 200
    body = res.json()
    assert body["summary"]["total_candidates"] == 1

    candidate = body["candidates"][0]
    assert candidate["candidate_name"] == "Aditi Rao"
    assert candidate["job_id"] == job["id"]
    assert candidate["ai_score"] is not None
    assert 0 <= candidate["ai_score"] <= 100
    assert candidate["ai_score"] >= 75  # full skill coverage -> high score
    assert candidate["matching_factors"] == "Strong match"
    assert candidate["ai_evaluation_label"] == "Shortlisted"
    assert candidate["status_label"] == "Shortlisted"
    assert body["summary"]["shortlisted"] == 1


def test_weak_match_candidate_gets_low_score_and_rejected(client):
    _add_recruiter(client, "9812430003")
    recruiter_headers = _login(client, "9812430003")

    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
            "required_skills": ["Python", "SQL", "Django", "Kubernetes"],
        },
        headers=recruiter_headers,
    ).json()

    student_headers = _register_student(client, "9812430004")
    _complete_profile_and_apply(client, student_headers, job["id"], ["Photoshop"])

    res = client.get("/api/recruiters/me/candidates", headers=recruiter_headers)
    candidate = res.json()["candidates"][0]
    assert candidate["ai_score"] < 45
    assert candidate["matching_factors"] == "Skill gaps"
    assert candidate["ai_evaluation_label"] == "Rejected"


def test_evaluation_is_idempotent_across_repeated_page_loads(client):
    _add_recruiter(client, "9812430005")
    recruiter_headers = _login(client, "9812430005")

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
    student_headers = _register_student(client, "9812430006")
    _complete_profile_and_apply(client, student_headers, job["id"], ["Python"])

    first = client.get("/api/recruiters/me/candidates", headers=recruiter_headers).json()
    second = client.get("/api/recruiters/me/candidates", headers=recruiter_headers).json()
    assert first["candidates"][0]["ai_score"] == second["candidates"][0]["ai_score"]


def test_candidate_workflow_shows_completed_ai_stages_and_pending_human_stages(client):
    _add_recruiter(client, "9812430007")
    recruiter_headers = _login(client, "9812430007")

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
    student_headers = _register_student(client, "9812430008")
    application = _complete_profile_and_apply(client, student_headers, job["id"], ["Python"])

    res = client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=recruiter_headers
    )
    assert res.status_code == 200
    body = res.json()

    assert body["selected_candidate"]["candidate_name"] == "Aditi Rao"
    assert body["selected_candidate"]["applied_role"] == "Backend Developer"
    assert body["selected_candidate"]["ai_score"] is not None

    stage_states = {s["key"]: s["state"] for s in body["stages"]}
    assert stage_states["resume_parser"] == "completed"
    assert stage_states["embedding"] == "completed"
    assert stage_states["matching"] == "completed"
    assert stage_states["shortlisting"] == "completed"
    # Human Approval (Phase 14) and Interview/Email (Phase 15) don't exist
    # yet, so these must never be silently marked as done.
    assert stage_states["human_approval"] == "pending"
    assert stage_states["interview"] == "pending"
    assert stage_states["email_invitation"] == "pending"


def test_candidate_filters_and_search(client):
    _add_recruiter(client, "9812430009")
    recruiter_headers = _login(client, "9812430009")

    job_a = client.post(
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
    job_b = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Frontend Engineer",
            "job_role": "Frontend Developer",
            "experience_required": "Entry Level",
            "required_skills": ["React"],
        },
        headers=recruiter_headers,
    ).json()

    s1 = _register_student(client, "9812430010")
    _complete_profile_and_apply(client, s1, job_a["id"], ["Python"])
    s2 = _register_student(client, "9812430011")
    _complete_profile_and_apply(client, s2, job_b["id"], ["JavaScript"])

    res = client.get(
        "/api/recruiters/me/candidates", params={"job_id": job_a["id"]}, headers=recruiter_headers
    )
    candidates = res.json()["candidates"]
    assert len(candidates) == 1
    assert candidates[0]["job_id"] == job_a["id"]

    res = client.get(
        "/api/recruiters/me/candidates",
        params={"ai_evaluation": "Rejected"},
        headers=recruiter_headers,
    )
    assert len(res.json()["candidates"]) == 1
    assert res.json()["candidates"][0]["job_id"] == job_b["id"]

    res = client.get(
        "/api/recruiters/me/candidates", params={"search": "Aditi"}, headers=recruiter_headers
    )
    assert len(res.json()["candidates"]) == 2  # both applicants share the same demo full_name


def test_candidate_workflow_requires_ownership(client):
    _add_recruiter(client, "9812430012")
    _add_recruiter(client, "9812430013")
    headers_a = _login(client, "9812430012")
    headers_b = _login(client, "9812430013")

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
    student_headers = _register_student(client, "9812430014")
    application = _complete_profile_and_apply(client, student_headers, job["id"], ["Python"])

    res = client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=headers_b
    )
    assert res.status_code == 404


def test_recruiter_candidates_requires_recruiter_role(client):
    headers = _register_student(client, "9812430015")
    res = client.get("/api/recruiters/me/candidates", headers=headers)
    assert res.status_code == 403
