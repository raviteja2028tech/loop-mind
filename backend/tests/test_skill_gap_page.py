"""Tests for the Skill Gap Analysis page endpoints — phase.md Phase 08.
The underlying analysis compute/store logic is Phase 06's; these tests
cover the page-shaping layer: empty state, auto-run-on-load, target
selection, role options, and Dashboard/Skill-Gap target-company sync.
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
    from backend.core.database import get_db
    from backend.main import app

    db = next(app.dependency_overrides[get_db]())
    seed_company_intelligence(db)
    ingest_company_intelligence_into_qdrant(db)


def test_skill_gap_page_empty_state_before_target_is_set(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812350001")

    res = client.get("/api/students/me/skill-gap", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["target_company"] is None
    assert body["readiness"]["has_analysis"] is False
    assert body["skills"] == []
    assert body["priority_areas"] == []
    assert "Nexora Technologies" in body["company_options"]


def test_setting_target_runs_analysis_and_shapes_the_page(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812350002")

    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Data Structures & Algorithms",
            "skill_category": "Core CS",
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

    res = client.put(
        "/api/students/me/skill-gap/target",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["target_company"] == "Nexora Technologies"
    assert body["target_role"] == "Software Engineer"
    assert "SDE Intern" in body["role_options"]

    assert body["readiness"]["has_analysis"] is True
    assert 0 <= body["readiness"]["readiness_percentage"] <= 100

    # DSA: Advanced, required Advanced, but no evidence was ever attached
    # -> Missing Evidence (Student Portal UPDATE SDD §6: a claimed-and-met
    # skill with no supporting evidence must not be shown as fully
    # verified "Strong"). Java: Beginner, required Advanced -> To Improve.
    # System Design/SQL: not in profile -> Missing.
    by_skill = {row["skill"]: row for row in body["skills"]}
    assert by_skill["Data Structures & Algorithms"]["status"] == "Missing Evidence"
    assert by_skill["Data Structures & Algorithms"]["your_level"] == "Advanced"
    assert by_skill["Data Structures & Algorithms"]["category"] == "Core CS"
    assert by_skill["Java"]["status"] == "To Improve"
    assert by_skill["Java"]["required_level"] == "Advanced"
    assert by_skill["System Design"]["status"] == "Missing"
    assert by_skill["System Design"]["resources"] is not None

    assert body["overview"]["total_required_skills"] == 4  # DSA, System Design, SQL, Java
    # Skill Gap/Profile Photo/Resume Management UPDATE SDD §1: "Skills You
    # Have" is the student's own current skill count (DSA + Java = 2),
    # not "how many required skills they already meet at the required
    # level" (that narrower, role-relative count is what the "Already
    # Strong" distribution bucket below measures).
    assert body["overview"]["skills_you_have"] == 2
    assert body["distribution"]["already_strong"] == 1
    assert body["overview"]["missing_evidence"] == 1
    assert body["distribution"]["missing"] == 2
    assert len(body["priority_areas"]) >= 1
    assert body["priority_areas"][0]["impact"] in ("High Impact", "Medium Impact", "Low Impact")


def test_skill_gap_page_auto_runs_when_target_already_set_via_dashboard(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812350003")

    client.put(
        "/api/students/me/target-company",
        json={"company_name": "Nexora Technologies"},
        headers=headers,
    )

    res = client.get("/api/students/me/skill-gap", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["target_company"] == "Nexora Technologies"
    assert body["readiness"]["has_analysis"] is True

    # Setting the target on the Skill Gap page must be visible from the
    # Dashboard too — both read/write the same Career/Placement record.
    dash = client.get("/api/students/me/dashboard", headers=headers)
    assert dash.json()["target_company"] == "Nexora Technologies"


def test_role_options_endpoint(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812350004")

    res = client.get(
        "/api/students/me/skill-gap/role-options",
        params={"company_name": "Nexora Technologies"},
        headers=headers,
    )
    assert res.status_code == 200
    assert set(res.json()) == {"Software Engineer", "SDE Intern"}


def test_skill_gap_target_unknown_company_returns_404(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812350005")

    res = client.put(
        "/api/students/me/skill-gap/target",
        json={"company_name": "Not A Real Company"},
        headers=headers,
    )
    assert res.status_code == 404


def test_skill_gap_page_requires_student_role(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9999999999", "purpose": "login"}
    )
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": "9999999999", "code": otp, "purpose": "login"},
    )
    headers = {"Authorization": f"Bearer {res.json()['token']}"}
    res = client.get("/api/students/me/skill-gap", headers=headers)
    assert res.status_code == 403
