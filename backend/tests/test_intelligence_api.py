"""End-to-end API tests for the Phase 06 intelligence endpoints: register
a student, build a real profile, and drive skill-gap/preparation-plan/
what-if through HTTP exactly as the frontend eventually will (Phase 08/09).
"""

from backend.core.seed_company_intelligence import seed_company_intelligence
from backend.services.intelligence_service import ingest_company_intelligence_into_qdrant
from backend.tests.conftest import complete_registration


def _register(client, mobile: str) -> dict:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "register"}
    )
    token = complete_registration(client, mobile, res.json()["token"])
    return {"Authorization": f"Bearer {token}"}


def _seed_company_intelligence(client):
    # Reuse the same DB the `client` fixture's override points at.
    from backend.core.database import get_db
    from backend.main import app

    db = next(app.dependency_overrides[get_db]())
    seed_company_intelligence(db)
    ingest_company_intelligence_into_qdrant(db)


def test_skill_gap_analysis_end_to_end(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812349001")

    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Data Structures & Algorithms",
            "skill_category": "Data Structures & Algorithms",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=headers,
    )
    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Java",
            "skill_category": "Programming Language",
            "proficiency": "Beginner",
            "learning_status": "Learning",
        },
        headers=headers,
    )

    res = client.post(
        "/api/students/me/skill-gap-analysis",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["target_company"] == "Nexora Technologies"
    assert "Data Structures & Algorithms" in body["analysis"]["skill_gap"]["existing_skills"]
    assert "Java" in body["analysis"]["skill_gap"]["weak_skills"]
    assert "System Design" in body["analysis"]["skill_gap"]["missing_skills"]
    assert 0 <= body["analysis"]["readiness"]["readiness_percentage"] <= 100


def test_skill_gap_analysis_unknown_company_returns_404(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812349002")
    res = client.post(
        "/api/students/me/skill-gap-analysis",
        json={"company_name": "Not A Real Company", "target_role": None},
        headers=headers,
    )
    assert res.status_code == 404


def test_preparation_plan_versioning_through_api(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812349003")
    client.put(
        "/api/students/me/academic-info",
        json={
            "college": "Test College",
            "degree": "B.Tech",
            "branch": "Computer Science",
            "academic_year": "2023-2027",
            "current_year": "1st Year",
            "current_semester": "1st Semester",
            "admission_year": "2023",
            "expected_graduation_year": "2027",
            "current_cgpa": 7.5,
            "cgpa_scale": "10",
        },
        headers=headers,
    )

    res1 = client.post(
        "/api/students/me/preparation-plan",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res1.status_code == 200
    assert res1.json()["version"] == 1
    assert res1.json()["status"] == "current"
    assert res1.json()["plan"]["horizon_summary"] == "long-term"  # 1st Year

    res2 = client.post(
        "/api/students/me/preparation-plan",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res2.status_code == 200
    assert res2.json()["version"] == 2
    assert res2.json()["status"] == "current"


def test_what_if_end_to_end(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812349004")

    res = client.post(
        "/api/students/me/what-if",
        json={
            "company_name": "Nexora Technologies",
            "target_role": "Software Engineer",
            "question": "What if I learn System Design?",
        },
        headers=headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["question"] == "What if I learn System Design?"
    assert body["result"]["topic"] == "System Design"
    assert body["result"]["relevant_to_target"] is True


def test_intelligence_endpoints_require_student_role(client):
    _seed_company_intelligence(client)
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9999999999", "purpose": "login"}
    )
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": "9999999999", "code": otp, "purpose": "login"},
    )
    recruiter_headers = {"Authorization": f"Bearer {res.json()['token']}"}

    res = client.post(
        "/api/students/me/skill-gap-analysis",
        json={"company_name": "Nexora Technologies"},
        headers=recruiter_headers,
    )
    assert res.status_code == 403
