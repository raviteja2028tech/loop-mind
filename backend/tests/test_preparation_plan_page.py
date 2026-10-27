"""Tests for the Preparation Plan page endpoints — phase.md Phase 09.
The underlying generate/store action is Phase 06's; these tests cover
the page-shaping layer: empty state, generating from this page,
Dashboard/Skill-Gap target sync, plan-row shaping, and goal tracking.
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


def test_preparation_plan_page_empty_state(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812360101")

    res = client.get("/api/students/me/preparation-plan-page", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["target_company"] is None
    assert body["has_plan"] is False
    assert body["plan_items"] == []
    assert len(body["year_wise_focus"]) == 4
    assert all(not y["is_current"] for y in body["year_wise_focus"])
    assert len(body["recommendations"]) == 5
    assert "Nexora Technologies" in body["company_options"]


def test_generate_from_this_page_shapes_plan_and_syncs_target(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812360102")

    client.put(
        "/api/students/me/academic-info",
        json={
            "college": "Test College",
            "degree": "B.Tech",
            "branch": "CSE",
            "academic_year": "2023-2027",
            "current_year": "1st Year",
            "current_semester": "1st Semester",
            "admission_year": "2023",
            "expected_graduation_year": "2027",
            "current_cgpa": 8.0,
            "cgpa_scale": "10",
        },
        headers=headers,
    )

    res = client.post(
        "/api/students/me/preparation-plan-page/generate",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["target_company"] == "Nexora Technologies"
    assert body["has_plan"] is True
    assert body["plan_version"] == 1
    assert body["plan_status"] == "current"
    assert len(body["plan_items"]) > 0

    row = body["plan_items"][0]
    assert row["current_level"] == "Not Started"
    assert row["status"] == "Missing"
    assert row["filter_category"] in (
        "DSA",
        "Development",
        "System Design",
        "Databases",
        "Projects",
        "Other",
    )
    assert row["start_date"] <= row["end_date"]

    # 1st Year -> long-term horizon in the underlying agent.
    year_1 = next(y for y in body["year_wise_focus"] if y["year"] == "1st Year")
    assert year_1["is_current"] is True

    # Target set from THIS page must be visible from the Dashboard too.
    dash = client.get("/api/students/me/dashboard", headers=headers)
    assert dash.json()["target_company"] == "Nexora Technologies"


def test_regenerating_creates_a_new_version(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812360103")

    res1 = client.post(
        "/api/students/me/preparation-plan-page/generate",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res1.json()["plan_version"] == 1

    res2 = client.post(
        "/api/students/me/preparation-plan-page/generate",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res2.json()["plan_version"] == 2
    assert res2.json()["plan_status"] == "current"


def test_generate_unknown_company_returns_404(client):
    _seed_company_intelligence(client)
    headers = _register(client, "9812360104")

    res = client.post(
        "/api/students/me/preparation-plan-page/generate",
        json={"company_name": "Not A Real Company"},
        headers=headers,
    )
    assert res.status_code == 404


def test_goal_tracking_add_and_toggle(client):
    headers = _register(client, "9812360105")

    res = client.get("/api/students/me/preparation-plan-page/goals", headers=headers)
    assert res.json() == {"short_term_goals": [], "long_term_goals": []}

    res = client.post(
        "/api/students/me/preparation-plan-page/goals",
        json={"kind": "short_term", "text": "Finish 50 DSA problems"},
        headers=headers,
    )
    assert res.status_code == 200
    goals = res.json()["short_term_goals"]
    assert len(goals) == 1
    assert goals[0]["text"] == "Finish 50 DSA problems"
    assert goals[0]["completed"] is False

    goal_id = goals[0]["id"]
    res = client.put(
        f"/api/students/me/preparation-plan-page/goals/{goal_id}/toggle",
        params={"kind": "short_term"},
        headers=headers,
    )
    assert res.json()["short_term_goals"][0]["completed"] is True

    # The Preparation Plan page itself must reflect the stored goal.
    page = client.get("/api/students/me/preparation-plan-page", headers=headers)
    assert page.json()["short_term_goals"][0]["completed"] is True


def test_preparation_plan_page_requires_student_role(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9999999999", "purpose": "login"}
    )
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": "9999999999", "code": otp, "purpose": "login"},
    )
    headers = {"Authorization": f"Bearer {res.json()['token']}"}
    res = client.get("/api/students/me/preparation-plan-page", headers=headers)
    assert res.status_code == 403
