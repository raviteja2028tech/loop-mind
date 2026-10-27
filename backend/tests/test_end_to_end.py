"""Full End-to-End System Testing — phase.md Phase 23.

"No new features" — these tests exercise the three flows phase.md draws
as diagrams, each as one continuous journey through the real HTTP API
rather than isolated unit checks (which the other ~130 tests already
cover per-feature):

* the complete Student Intelligence flow (Authentication -> Student
  Profile -> Target Company/Role -> Company Intelligence -> Student
  Skill Analysis -> Placement Readiness -> Skill Gap -> What-If ->
  Preparation Plan -> Student Improvement);
* the complete recruitment flow (Student -> Jobs -> Application -> Resume
  -> Resume Parser -> Embedding -> Matching -> AI Shortlisting ->
  Recruiter Review -> Human Approval -> Interview Agent -> Email
  Invitation -> Interview -> Outcome);
* the closed loop (Recruitment Outcome -> Student -> Skill Gap ->
  Preparation -> Improvement -> Future Intelligence), both the approved
  and not-approved branches, tying Phases 10-17 together in one scenario.
"""

import io

from backend.core.seed_company_intelligence import seed_company_intelligence
from backend.models.recruiter import Recruiter
from backend.tests.conftest import complete_registration


def _db(client):
    from backend.core.database import get_db
    from backend.main import app

    return next(app.dependency_overrides[get_db]())


def _seed_company_intelligence(client):
    seed_company_intelligence(_db(client))


def _add_recruiter(client, mobile: str) -> None:
    db = _db(client)
    db.add(Recruiter(mobile_number=mobile, name="Fresh Recruiter"))
    db.commit()


def _register_student(client, mobile: str) -> dict:
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


def _add_skill(client, headers, name, category="Programming", proficiency="Advanced"):
    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": name,
            "skill_category": category,
            "proficiency": proficiency,
            "learning_status": "Confident",
        },
        headers=headers,
    )


def test_complete_student_intelligence_flow(client):
    _seed_company_intelligence(client)

    # Authentication (new account, OTP -> JWT).
    headers = _register_student(client, "9812510001")

    # Student Profile.
    res = client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Ananya Rao",
            "date_of_birth": "2003-04-12",
            "gender": "female",
            "email": "ananya@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=headers,
    )
    assert res.status_code == 200
    res = client.put(
        "/api/students/me/academic-info",
        json={
            "college": "PES University",
            "degree": "B.Tech",
            "branch": "CSE",
            "academic_year": "2022-2026",
            "current_year": "3",
            "current_semester": "6",
            "admission_year": "2022",
            "expected_graduation_year": "2026",
            "current_cgpa": 8.2,
            "cgpa_scale": "10",
        },
        headers=headers,
    )
    assert res.status_code == 200

    # Partial skill match against Nexora Technologies' Software Engineer
    # requirements (DSA Advanced, System Design Intermediate, SQL
    # Intermediate, Java Advanced) — deliberately has SQL and Java only,
    # so the gap analysis below has genuine matched AND missing skills.
    _add_skill(client, headers, "SQL", category="Databases")
    _add_skill(client, headers, "Java")

    # Target Company / Role -> triggers Company Intelligence, Student
    # Skill Analysis, Placement Readiness, Skill Gap and Preparation Plan
    # (Multi-Agent System 1, Agents 1-5) in one call.
    res = client.put(
        "/api/students/me/skill-gap/target",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert res.status_code == 200

    # Skill Gap (+ implicitly: Company Intelligence, Student Skill
    # Analysis, Placement Readiness).
    gap = client.get("/api/students/me/skill-gap", headers=headers).json()
    assert gap["target_company"] == "Nexora Technologies"
    assert gap["readiness"]["has_analysis"] is True
    readiness_before = gap["readiness"]["readiness_percentage"]
    assert 0 < readiness_before < 100  # partial match -> neither 0 nor 100
    skill_names = {s["skill"] for s in gap["skills"]}
    assert "SQL" in skill_names or "sql" in {s.lower() for s in skill_names}
    assert any(s["status"] == "Missing" for s in gap["skills"])
    assert len(gap["priority_areas"]) > 0

    # What-If.
    what_if = client.post(
        "/api/students/me/what-if",
        json={
            "company_name": "Nexora Technologies",
            "target_role": "Software Engineer",
            "question": "What if I learn Data Structures & Algorithms?",
        },
        headers=headers,
    )
    assert what_if.status_code == 200
    assert what_if.json()["question"]

    # Preparation Plan — the page's own explicit "Get Personalized Plan"
    # action (it never auto-generates merely from viewing the page).
    generated = client.post(
        "/api/students/me/preparation-plan-page/generate",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert generated.status_code == 200

    plan = client.get("/api/students/me/preparation-plan-page", headers=headers).json()
    assert plan["target_company"] == "Nexora Technologies"
    assert len(plan["year_wise_focus"]) > 0

    goals = client.post(
        "/api/students/me/preparation-plan-page/goals",
        json={"kind": "short_term", "text": "Finish a DSA course"},
        headers=headers,
    ).json()
    goal_id = goals["short_term_goals"][-1]["id"]
    assert goals["short_term_goals"][-1]["completed"] is False

    toggled = client.put(
        f"/api/students/me/preparation-plan-page/goals/{goal_id}/toggle",
        params={"kind": "short_term"},
        headers=headers,
    ).json()
    assert next(g for g in toggled["short_term_goals"] if g["id"] == goal_id)["completed"] is True

    regenerated = client.post(
        "/api/students/me/preparation-plan",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert regenerated.status_code == 200
    assert regenerated.json()["version"] >= 2  # a new version, not overwritten

    # Student Improvement: learn the previously-missing skill. The Skill
    # Gap page's existing/weak/missing buckets come from the last *stored*
    # analysis (auto-run-once-on-view, not recomputed on every view) — the
    # student re-submitting their target is the real, existing refresh
    # mechanism (there is no separate "just refresh" action), so that is
    # what actually re-runs the analysis against the improved profile.
    _add_skill(client, headers, "Data Structures & Algorithms")
    refreshed = client.put(
        "/api/students/me/skill-gap/target",
        json={"company_name": "Nexora Technologies", "target_role": "Software Engineer"},
        headers=headers,
    )
    assert refreshed.status_code == 200
    improved_gap = client.get("/api/students/me/skill-gap", headers=headers).json()
    improved_skill_row = next(
        s for s in improved_gap["skills"] if s["skill"] == "Data Structures & Algorithms"
    )
    assert improved_skill_row["status"] != "Missing"
    assert improved_gap["readiness"]["readiness_percentage"] >= readiness_before


def test_complete_recruitment_flow(client):
    _add_recruiter(client, "9812510002")
    recruiter_headers = _login(client, "9812510002")

    # Recruiter: job creation.
    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
            "required_skills": ["Python", "SQL"],
        },
        headers=recruiter_headers,
    )
    assert job.status_code == 200
    job = job.json()

    # Student -> Jobs -> Application -> Resume.
    student_headers = _register_student(client, "9812510003")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Rohit Verma",
            "date_of_birth": "2003-02-20",
            "gender": "male",
            "email": "rohit@example.com",
            "country": "India",
            "state": "Maharashtra",
            "city": "Pune",
        },
        headers=student_headers,
    )
    _add_skill(client, student_headers, "Python", category="Programming")
    _add_skill(client, student_headers, "SQL", category="Databases")
    resume = client.post(
        "/api/students/me/resume",
        headers=student_headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    assert resume.status_code == 200

    applied = client.post(f"/api/students/me/jobs/{job['id']}/apply", headers=student_headers)
    assert applied.status_code == 200
    application = applied.json()
    assert application["status_label"] == "Under Review"

    # Resume Parser -> Embedding -> Matching -> AI Shortlisting (Agents
    # 7-10), auto-run the moment the recruiter views their candidates.
    candidates = client.get("/api/recruiters/me/candidates", headers=recruiter_headers).json()
    candidate_row = candidates["candidates"][0]
    assert candidate_row["ai_score"] is not None
    assert candidate_row["ai_score"] >= 75  # full skill coverage -> a strong match
    assert candidate_row["ai_evaluation_label"] == "Shortlisted"

    # Recruiter Review -> Human Approval.
    workflow = client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=recruiter_headers
    ).json()
    assert workflow["human_decision"] is None  # AI alone never finalizes this
    approved = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    assert approved.status_code == 200
    assert approved.json()["human_decision"] == "approved"

    # Interview Agent — real, role-specific questions, generated exactly
    # because of the approval above, not because anyone viewed a page.
    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert len(detail["questions"]) > 0
    assert all(q["evaluation_criteria"] for q in detail["questions"])

    # Interview scheduling -> Email Invitation composed from real data.
    scheduled = client.post(
        f"/api/recruiters/me/interviews/{application['id']}/schedule",
        json={"interview_type": "Technical", "scheduled_at": "2026-11-01T10:00:00Z"},
        headers=recruiter_headers,
    )
    assert scheduled.status_code == 200
    scheduled_body = scheduled.json()
    assert scheduled_body["invitation_subject"] is not None
    assert "Backend Engineer" in scheduled_body["invitation_subject"]

    student_sees_invitation = client.get(
        "/api/students/me/jobs/applications", headers=student_headers
    ).json()
    assert student_sees_invitation[0]["status_label"] == "Interview Invitation"

    # Interview happens -> Outcome.
    completed = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/status",
        json={"status": "completed"},
        headers=recruiter_headers,
    )
    assert completed.status_code == 200
    outcome = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/outcome",
        json={"outcome": "hired"},
        headers=recruiter_headers,
    )
    assert outcome.status_code == 200
    assert outcome.json()["outcome_label"] == "Hired"


def test_closed_loop_both_branches(client):
    _add_recruiter(client, "9812510004")
    recruiter_headers = _login(client, "9812510004")

    job = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Data Engineer I",
            "job_role": "Data Engineer",
            "experience_required": "Entry Level",
            "required_skills": ["Python", "SQL"],
        },
        headers=recruiter_headers,
    ).json()

    # Branch 1 — approved all the way to Hired.
    hired_headers = _register_student(client, "9812510005")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Hired Candidate",
            "date_of_birth": "2003-01-01",
            "gender": "female",
            "email": "hired@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=hired_headers,
    )
    _add_skill(client, hired_headers, "Python")
    _add_skill(client, hired_headers, "SQL", category="Databases")
    client.post(
        "/api/students/me/resume",
        headers=hired_headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    hired_app = client.post(
        f"/api/students/me/jobs/{job['id']}/apply", headers=hired_headers
    ).json()
    client.post(
        f"/api/recruiters/me/candidates/{hired_app['id']}/approve", headers=recruiter_headers
    )
    client.post(
        f"/api/recruiters/me/interviews/{hired_app['id']}/schedule",
        json={"interview_type": "Technical", "scheduled_at": "2026-11-05T10:00:00Z"},
        headers=recruiter_headers,
    )
    client.put(
        f"/api/recruiters/me/interviews/{hired_app['id']}/status",
        json={"status": "completed"},
        headers=recruiter_headers,
    )
    client.put(
        f"/api/recruiters/me/interviews/{hired_app['id']}/outcome",
        json={"outcome": "hired"},
        headers=recruiter_headers,
    )

    # Recruitment Outcome -> Student sees it.
    hired_apps = client.get("/api/students/me/jobs/applications", headers=hired_headers).json()
    assert hired_apps[0]["status_label"] == "Hired"

    # Branch 2 — a second candidate for the *same role*, missing System
    # Design. Outcome -> Future Intelligence: the hire above must already
    # be shaping what this candidate's recruiter sees.
    job2 = client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Data Engineer II",
            "job_role": "Data Engineer",
            "experience_required": "Entry Level",
            "required_skills": ["Python", "SQL", "System Design"],
        },
        headers=recruiter_headers,
    ).json()
    not_selected_headers = _register_student(client, "9812510006")
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Not Selected Candidate",
            "date_of_birth": "2003-01-01",
            "gender": "male",
            "email": "notselected@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=not_selected_headers,
    )
    _add_skill(client, not_selected_headers, "Python")
    client.post(
        "/api/students/me/resume",
        headers=not_selected_headers,
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    not_selected_app = client.post(
        f"/api/students/me/jobs/{job2['id']}/apply", headers=not_selected_headers
    ).json()

    # Future Intelligence: the real historical signal from the hire above.
    workflow = client.get(
        f"/api/recruiters/me/candidates/{not_selected_app['id']}/workflow",
        headers=recruiter_headers,
    ).json()
    assert workflow["historical_signal"] is not None
    assert "Data Engineer" in workflow["historical_signal"]

    # Not-approved branch: disapprove with a specific skill gap.
    client.post(
        f"/api/recruiters/me/candidates/{not_selected_app['id']}/disapprove",
        json={"reason": "Skill Gap: System Design"},
        headers=recruiter_headers,
    )

    # Skill Gap -> Preparation -> Improvement: the student sees exactly
    # which skill to work on next, closing the not-approved loop.
    my_apps = client.get("/api/students/me/jobs/applications", headers=not_selected_headers).json()
    assert my_apps[0]["status_label"] == "Disapproved"
    assert my_apps[0]["disapproval_reason"] == "Skill Gap: System Design"

    # Improvement: the student learns the flagged skill.
    _add_skill(client, not_selected_headers, "System Design")
    skills = client.get("/api/students/me/skills", headers=not_selected_headers).json()
    assert any(s["skill_name"] == "System Design" for s in skills)
