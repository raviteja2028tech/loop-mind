"""Tests for the Student Dashboard aggregation endpoint — phase.md Phase
07: layout is fixed elsewhere (frontend), but every value here must be
calculated from actual stored data, never hardcoded.
"""

from backend.core.seed_company_intelligence import seed_company_intelligence
from backend.tests.conftest import complete_registration


def _seed_companies(client):
    from backend.core.database import get_db
    from backend.main import app

    db = next(app.dependency_overrides[get_db]())
    seed_company_intelligence(db)


def _register(client, mobile: str) -> dict:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "register"}
    )
    token = complete_registration(client, mobile, res.json()["token"])
    return {"Authorization": f"Bearer {token}"}


def test_dashboard_starts_near_zero_for_a_brand_new_student(client):
    # Student Create Account UPDATE SDD: a real student account only ever
    # exists once Create Account has run, which requires Basic Information
    # + consent to already be set — `complete_registration`'s placeholder
    # values are what a freshly created account genuinely starts with
    # (1 of 6 profile-completion sections; a "Completed Basic Information"
    # recent-activity entry), not an all-zero, nothing-saved-yet state.
    headers = _register(client, "9812360001")
    res = client.get("/api/students/me/dashboard", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["full_name"] == "Test Student"
    assert body["profile_completion_percentage"] == 17
    assert body["skills_count"] == 0
    assert body["target_company"] is None
    assert body["placement_readiness"]["has_analysis"] is False
    assert len(body["recent_activity"]) == 1
    assert all(not stage["complete"] for stage in body["preparation_journey"])
    assert len(body["recommended_for_you"]) == 4
    assert len(body["upcoming_tasks"]) <= 4


def test_dashboard_reflects_real_profile_progress(client):
    headers = _register(client, "9812360002")

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
    client.put(
        "/api/students/me/academic-info",
        json={
            "college": "Test College",
            "degree": "B.Tech",
            "branch": "CSE",
            "academic_year": "2023-2027",
            "current_year": "2nd Year",
            "current_semester": "3rd Semester",
            "admission_year": "2023",
            "expected_graduation_year": "2027",
            "current_cgpa": 8.0,
            "cgpa_scale": "10",
        },
        headers=headers,
    )
    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Language",
            "proficiency": "Intermediate",
            "learning_status": "Learning",
        },
        headers=headers,
    )
    client.post(
        "/api/students/me/projects",
        json={"project_name": "Portfolio Site"},
        headers=headers,
    )

    res = client.get("/api/students/me/dashboard", headers=headers)
    body = res.json()
    assert body["full_name"] == "Priya Sharma"
    assert body["skills_count"] == 1
    assert body["projects_count"] == 1
    # 4 of 6 sections done (basic, academic, skills, projects) = 67%
    assert body["profile_completion_percentage"] == 67
    assert body["preparation_journey"][1]["complete"] is True  # Learn: has a skill

    labels = [a["label"] for a in body["recent_activity"]]
    assert "Completed Basic Information" in labels
    assert "Added a new project" in labels


def test_target_company_empty_state_then_set(client):
    _seed_companies(client)
    headers = _register(client, "9812360003")

    res = client.get("/api/students/me/target-company", headers=headers)
    assert res.json() == {"company_name": None}

    res = client.get("/api/students/me/company-options", headers=headers)
    names = [c["name"] for c in res.json()]
    assert "Nexora Technologies" in names

    res = client.put(
        "/api/students/me/target-company",
        json={"company_name": "Nexora Technologies"},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json() == {"company_name": "Nexora Technologies"}

    res = client.get("/api/students/me/dashboard", headers=headers)
    assert res.json()["target_company"] == "Nexora Technologies"
    assert "Explore companies" not in [t["label"] for t in res.json()["upcoming_tasks"]]


def test_dashboard_reflects_skill_gap_analysis_once_run(client):
    _seed_companies(client)
    headers = _register(client, "9812360004")
    # Placement Readiness Percentage UPDATE SDD §4 "Single Source of
    # Truth": the Dashboard's readiness is now scoped to the student's
    # *current target company* (same as Skill Gap/Preparation Plan), not
    # just "whatever analysis happens to exist" — so a target must
    # actually be set for the freshly run analysis to surface here.
    client.put(
        "/api/students/me/target-company",
        json={"company_name": "Nexora Technologies"},
        headers=headers,
    )
    client.post(
        "/api/students/me/skill-gap-analysis",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    res = client.get("/api/students/me/dashboard", headers=headers)
    readiness = res.json()["placement_readiness"]
    assert readiness["has_analysis"] is True
    assert isinstance(readiness["readiness_percentage"], int)
    assert len(res.json()["recommended_for_you"]) == 4  # still exactly 4, now gap-driven


def test_dashboard_requires_student_role(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9999999999", "purpose": "login"}
    )
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": "9999999999", "code": otp, "purpose": "login"},
    )
    headers = {"Authorization": f"Bearer {res.json()['token']}"}
    res = client.get("/api/students/me/dashboard", headers=headers)
    assert res.status_code == 403
