"""Tests for Recruiter Job Management & Create New Job — phase.md Phase
12. The most important requirement here is cross-portal: a job created by
a recruiter must become visible/applicable on the Student Jobs page with
no separate sync step, since both portals read the same `Job` table.
"""

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


def test_job_management_starts_empty_for_a_fresh_recruiter(client):
    _add_recruiter(client, "9812410001")
    headers = _login(client, "9812410001")

    res = client.get("/api/recruiters/me/jobs", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["summary"] == {
        "total_jobs": 0,
        "active_jobs": 0,
        "paused_jobs": 0,
        "total_applications": 0,
    }
    assert body["jobs"] == []


def test_create_job_appears_in_management_and_updates_summary(client):
    _add_recruiter(client, "9812410002")
    headers = _login(client, "9812410002")

    res = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
            "required_skills": ["Python", "SQL"],
        },
        headers=headers,
    )
    assert res.status_code == 200
    job = res.json()
    assert job["job_title"] == "Backend Engineer"
    assert job["status"] == "Active"
    assert job["applications"] == 0

    page = client.get("/api/recruiters/me/jobs", headers=headers).json()
    assert page["summary"]["total_jobs"] == 1
    assert page["summary"]["active_jobs"] == 1
    assert len(page["jobs"]) == 1
    assert page["jobs"][0]["id"] == job["id"]


def test_created_job_is_immediately_visible_and_applicable_on_student_jobs_page(client):
    _add_recruiter(client, "9812410003")
    recruiter_headers = _login(client, "9812410003")

    created = client.post(
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

    student_headers = _register_student(client, "9812410004")
    student_jobs = client.get("/api/students/me/jobs", headers=student_headers).json()["jobs"]
    matching = next((j for j in student_jobs if j["id"] == created["id"]), None)
    assert matching is not None
    assert matching["company_name"] == "Acme Robotics"
    assert matching["job_title"] == "Backend Engineer"
    assert matching["required_skills"] == ["Python", "SQL"]

    # And a student can actually apply to it — the cross-portal flow spec.md requires.
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Test Student",
            "date_of_birth": "2003-01-01",
            "gender": "female",
            "email": "t@example.com",
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
        files={"file": ("r.pdf", io.BytesIO(b"%PDF-1.4"), "application/pdf")},
    )
    apply_res = client.post(f"/api/students/me/jobs/{created['id']}/apply", headers=student_headers)
    assert apply_res.status_code == 200

    recruiter_view = client.get("/api/recruiters/me/jobs", headers=recruiter_headers).json()
    assert recruiter_view["jobs"][0]["applications"] == 1
    assert recruiter_view["summary"]["total_applications"] == 1


def test_search_and_status_filter(client):
    _add_recruiter(client, "9812410005")
    headers = _login(client, "9812410005")

    client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
        },
        headers=headers,
    )
    second = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Frontend Engineer",
            "job_role": "Frontend Developer",
            "experience_required": "Entry Level",
        },
        headers=headers,
    ).json()

    res = client.get("/api/recruiters/me/jobs", params={"search": "Frontend"}, headers=headers)
    jobs = res.json()["jobs"]
    assert len(jobs) == 1
    assert jobs[0]["job_title"] == "Frontend Engineer"

    client.put(
        f"/api/recruiters/me/jobs/{second['id']}/status",
        json={"status": "paused"},
        headers=headers,
    )
    res = client.get("/api/recruiters/me/jobs", params={"status": "active"}, headers=headers)
    assert len(res.json()["jobs"]) == 1
    res = client.get("/api/recruiters/me/jobs", params={"status": "paused"}, headers=headers)
    assert len(res.json()["jobs"]) == 1
    assert res.json()["jobs"][0]["status"] == "Paused"


def test_recruiter_cannot_manage_another_recruiters_job(client):
    _add_recruiter(client, "9812410006")
    _add_recruiter(client, "9812410007")
    headers_a = _login(client, "9812410006")
    headers_b = _login(client, "9812410007")

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


def test_recruiter_jobs_requires_recruiter_role(client):
    headers = _register_student(client, "9812410008")
    res = client.get("/api/recruiters/me/jobs", headers=headers)
    assert res.status_code == 403
