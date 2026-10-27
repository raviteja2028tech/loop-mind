"""Tests for the Student Jobs & Application System — phase.md Phase 10."""

import io

from backend.core.seed_jobs import seed_jobs
from backend.tests.conftest import complete_registration


def _register(client, mobile: str) -> dict:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "register"}
    )
    token = complete_registration(client, mobile, res.json()["token"])
    return {"Authorization": f"Bearer {token}"}


def _seed_jobs(client):
    from backend.core.database import get_db
    from backend.main import app

    db = next(app.dependency_overrides[get_db]())
    seed_jobs(db)


def _complete_basic_info(client, headers):
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Priya Sharma",
            "date_of_birth": "2003-06-15",
            "gender": "female",
            "email": "priya@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=headers,
    )


def test_jobs_page_lists_seeded_jobs_with_summary_and_filters(client):
    _seed_jobs(client)
    headers = _register(client, "9812380001")

    res = client.get("/api/students/me/jobs", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["summary"]["total_jobs"] > 0
    assert body["summary"]["applied"] == 0
    assert "Nexora Technologies" in body["filters"]["companies"]
    assert len(body["jobs"]) == body["summary"]["total_jobs"]
    first = body["jobs"][0]
    assert first["is_saved"] is False
    assert first["has_applied"] is False
    assert first["posted_relative"].startswith("Posted")


def test_search_and_filter_work_together(client):
    _seed_jobs(client)
    headers = _register(client, "9812380002")

    res = client.get(
        "/api/students/me/jobs",
        params={"search": "React", "company": "BluePeak Software"},
        headers=headers,
    )
    jobs = res.json()["jobs"]
    assert len(jobs) == 1
    assert jobs[0]["company_name"] == "BluePeak Software"
    assert jobs[0]["job_role"] == "Frontend Developer"

    res = client.get(
        "/api/students/me/jobs",
        params={"company": "Not A Real Company"},
        headers=headers,
    )
    assert res.json()["jobs"] == []


def test_save_toggle_is_persistent(client):
    _seed_jobs(client)
    headers = _register(client, "9812380003")

    jobs = client.get("/api/students/me/jobs", headers=headers).json()["jobs"]
    job_id = jobs[0]["id"]

    res = client.post(f"/api/students/me/jobs/{job_id}/save", headers=headers)
    assert res.json() == {"saved": True}

    jobs = client.get("/api/students/me/jobs", headers=headers).json()["jobs"]
    assert next(j for j in jobs if j["id"] == job_id)["is_saved"] is True

    res = client.post(f"/api/students/me/jobs/{job_id}/save", headers=headers)
    assert res.json() == {"saved": False}
    jobs = client.get("/api/students/me/jobs", headers=headers).json()["jobs"]
    assert next(j for j in jobs if j["id"] == job_id)["is_saved"] is False


def test_apply_blocked_when_resume_missing(client):
    _seed_jobs(client)
    headers = _register(client, "9812380004")
    _complete_basic_info(client, headers)

    jobs = client.get("/api/students/me/jobs", headers=headers).json()["jobs"]
    job_id = jobs[0]["id"]

    res = client.post(f"/api/students/me/jobs/{job_id}/apply", headers=headers)
    assert res.status_code == 409
    missing_fields = [m["field"] for m in res.json()["detail"]["missing"]]
    assert "resume" in missing_fields
    assert "full_name" not in missing_fields  # already completed above


def test_upload_resume_then_apply_succeeds(client):
    _seed_jobs(client)
    headers = _register(client, "9812380005")
    _complete_basic_info(client, headers)

    res = client.post(
        "/api/students/me/resume",
        headers=headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    assert res.status_code == 200
    assert res.json()["resume_file_path"] is not None

    jobs = client.get("/api/students/me/jobs", headers=headers).json()["jobs"]
    job_id = jobs[0]["id"]

    res = client.post(f"/api/students/me/jobs/{job_id}/apply", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["job_id"] == job_id
    assert body["status_label"] == "Under Review"

    # Re-applying to the same job returns the existing application, not a duplicate.
    res2 = client.post(f"/api/students/me/jobs/{job_id}/apply", headers=headers)
    assert res2.json()["id"] == body["id"]

    summary = client.get("/api/students/me/jobs", headers=headers).json()["summary"]
    assert summary["applied"] == 1
    assert summary["under_review"] == 1

    my_apps = client.get("/api/students/me/jobs/applications", headers=headers).json()
    assert len(my_apps) == 1
    assert my_apps[0]["job_id"] == job_id


def test_resume_upload_rejects_non_pdf(client):
    headers = _register(client, "9812380006")
    res = client.post(
        "/api/students/me/resume",
        headers=headers,
        files={"file": ("resume.txt", io.BytesIO(b"not a pdf"), "text/plain")},
    )
    assert res.status_code == 400


def test_jobs_page_requires_student_role(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9999999999", "purpose": "login"}
    )
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": "9999999999", "code": otp, "purpose": "login"},
    )
    headers = {"Authorization": f"Bearer {res.json()['token']}"}
    res = client.get("/api/students/me/jobs", headers=headers)
    assert res.status_code == 403
