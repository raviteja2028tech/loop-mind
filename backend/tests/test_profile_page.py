"""Tests for My Profile / Student Progress — phase.md Phase 18.

spec.md §26 "Dynamic Data Rule" is the core requirement this file checks:
every number (completion %, stats, missing fields, recruitment history)
must change in response to real stored data, never a hardcoded value —
and every section is isolated per-student (spec.md §21 data isolation).
"""

import io

from backend.tests.conftest import complete_registration


def _register(client, mobile: str) -> dict:
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


def _complete_basic_info(client, headers, full_name="Priya Sharma"):
    return client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": full_name,
            "date_of_birth": "2003-06-15",
            "gender": "female",
            "email": "priya@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=headers,
    )


def _complete_academic_info(client, headers):
    return client.put(
        "/api/students/me/academic-info",
        json={
            "college": "PES University",
            "degree": "B.Tech",
            "branch": "CSE",
            "academic_year": "2024-2028",
            "current_year": "2",
            "current_semester": "4",
            "admission_year": "2024",
            "expected_graduation_year": "2028",
            "current_cgpa": 8.5,
            "cgpa_scale": "10",
        },
        headers=headers,
    )


def test_profile_page_empty_for_fresh_student(client):
    # Student Create Account UPDATE SDD: Create Account requires Basic
    # Information + consent to already be set, so a freshly created
    # account starts with those two sections done (2 of 10 = 20%), not
    # all sections missing.
    headers = _register(client, "9812490001")
    res = client.get("/api/students/me/profile", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["completion_percentage"] == 20
    assert body["stats"]["skills_added"] == 0
    assert len(body["missing_fields"]) == 8


def test_profile_page_completion_grows_with_real_data(client):
    headers = _register(client, "9812490002")
    _complete_basic_info(client, headers)
    _complete_academic_info(client, headers)
    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=headers,
    )

    res = client.get("/api/students/me/profile", headers=headers)
    body = res.json()
    assert body["completion_percentage"] == 40  # basic + consent + academic + skills
    assert body["overview"]["full_name"] == "Priya Sharma"
    assert body["overview"]["degree"] == "B.Tech"
    assert body["stats"]["skills_added"] == 1
    missing_sections = {m["section"] for m in body["missing_fields"]}
    assert "Basic Information" not in missing_sections
    assert "Career & Placement" in missing_sections


def test_profile_page_isolated_per_student(client):
    headers_a = _register(client, "9812490003")
    headers_b = _register(client, "9812490004")
    _complete_basic_info(client, headers_a, full_name="Student A")

    res_a = client.get("/api/students/me/profile", headers=headers_a).json()
    res_b = client.get("/api/students/me/profile", headers=headers_b).json()
    assert res_a["overview"]["full_name"] == "Student A"
    # B's account has its own placeholder Basic Information from
    # registration — the isolation property under test is that it's B's
    # own data, never A's.
    assert res_b["overview"]["full_name"] == "Test Student"


def test_skill_edit(client):
    headers = _register(client, "9812490005")
    created = client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Beginner",
            "learning_status": "Learning",
        },
        headers=headers,
    ).json()

    res = client.put(
        f"/api/students/me/skills/{created['id']}",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["proficiency"] == "Advanced"

    skills = client.get("/api/students/me/skills", headers=headers).json()
    assert len(skills) == 1  # edited, not duplicated
    assert skills[0]["proficiency"] == "Advanced"


def test_skill_edit_requires_ownership(client):
    headers_a = _register(client, "9812490006")
    headers_b = _register(client, "9812490007")
    created = client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Beginner",
            "learning_status": "Learning",
        },
        headers=headers_a,
    ).json()

    res = client.put(
        f"/api/students/me/skills/{created['id']}",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=headers_b,
    )
    assert res.status_code == 404


def test_career_placement_learning_professional_consent_round_trip(client):
    headers = _register(client, "9812490008")

    res = client.put(
        "/api/students/me/career-placement",
        json={"target_company": "Google", "target_role": "SDE", "placement_interest": "Yes"},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["target_company"] == "Google"

    res = client.put(
        "/api/students/me/learning-preparation",
        json={
            "current_preparation_status": "In Progress",
            "current_learning_areas": ["DSA", "System Design"],
        },
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["current_preparation_status"] == "In Progress"

    res = client.put(
        "/api/students/me/professional-links",
        json={
            "github_url": "https://github.com/priya",
            "linkedin_url": "https://linkedin.com/in/priya",
        },
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["github_url"] == "https://github.com/priya"

    res = client.put(
        "/api/students/me/consent",
        json={
            "consent_use_information": True,
            "consent_learning_experience": True,
            "consent_anonymized_intelligence": False,
        },
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["consent_use_information"] is True
    assert res.json()["consent_anonymized_intelligence"] is False

    # Profile page must reflect the newly-completed sections.
    page = client.get("/api/students/me/profile", headers=headers).json()
    missing_sections = {m["section"] for m in page["missing_fields"]}
    assert "Career & Placement" not in missing_sections
    assert "Learning & Preparation" not in missing_sections
    assert "Consent & Knowledge Sharing" not in missing_sections


def test_recruitment_history_reflects_real_applications(client):
    from backend.models.recruiter import Recruiter

    def _db(client):
        from backend.core.database import get_db
        from backend.main import app

        return next(app.dependency_overrides[get_db]())

    db = _db(client)
    db.add(Recruiter(mobile_number="9812490009", name="Fresh Recruiter"))
    db.commit()
    recruiter_headers = _login(client, "9812490009")
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

    student_headers = _register(client, "9812490010")
    _complete_basic_info(client, student_headers, full_name="Recruitment History Student")
    client.post(
        "/api/students/me/resume",
        headers=student_headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    application = client.post(
        f"/api/students/me/jobs/{job['id']}/apply", headers=student_headers
    ).json()

    history = client.get("/api/students/me/recruitment-history", headers=student_headers).json()
    assert history["total_applications"] == 1
    assert history["companies_applied_to"] == ["Acme Robotics"]
    assert history["applications"][0]["recruitment_stage_reached"] == "Under Review"

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    history = client.get("/api/students/me/recruitment-history", headers=student_headers).json()
    assert history["applications"][0]["recruitment_stage_reached"] in ("Approved", "Interview")


def test_delete_account_removes_profile_data(client):
    headers = _register(client, "9812490011")
    _complete_basic_info(client, headers, full_name="To Be Deleted")
    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Programming",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=headers,
    )

    res = client.delete("/api/students/me/account", headers=headers)
    assert res.status_code == 200
    assert res.json()["deleted"] is True

    # The account's data is gone from the database. Tokens are stateless
    # JWTs with no revocation list anywhere in this system (every route
    # behaves this way, not just this one), so the same token still
    # authenticates — it just has nothing left to read.
    res = client.get("/api/students/me/profile", headers=headers)
    assert res.status_code == 200
    assert res.json()["overview"]["full_name"] is None
    assert res.json()["stats"]["skills_added"] == 0


def test_profile_endpoints_require_student_role(client):
    from backend.models.recruiter import Recruiter

    def _db(client):
        from backend.core.database import get_db
        from backend.main import app

        return next(app.dependency_overrides[get_db]())

    db = _db(client)
    db.add(Recruiter(mobile_number="9812490012", name="Fresh Recruiter"))
    db.commit()
    recruiter_headers = _login(client, "9812490012")

    res = client.get("/api/students/me/profile", headers=recruiter_headers)
    assert res.status_code == 403
