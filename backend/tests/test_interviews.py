"""Tests for the Interview Agent, Email Agent & Interviews Page — phase.md
Phase 15.

The critical requirement here is spec.md's boundary: interview question
generation must be triggered by the recruiter-approval event, never by
merely viewing a page — `test_approval_triggers_question_generation` and
`test_viewing_candidates_page_does_not_generate_questions` exercise that
distinction directly. AI Status (question-generation state) and Interview
Status (scheduling lifecycle) must also stay separate columns, never
merged — `test_ai_status_and_interview_status_stay_separate` checks that.
"""

import io
from unittest.mock import patch

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


def _apply_with_skills(client, student_headers, job_id, skills):
    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Kavya Nair",
            "date_of_birth": "2003-03-03",
            "gender": "female",
            "email": "kavya@example.com",
            "country": "India",
            "state": "Kerala",
            "city": "Kochi",
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


def _make_job(client, recruiter_headers, skills):
    return client.post(
        "/api/recruiters/me/jobs",
        json={
            "company_name": "Acme Robotics",
            "job_title": "Backend Engineer",
            "job_role": "Backend Developer",
            "experience_required": "Entry Level",
            "required_skills": skills,
        },
        headers=recruiter_headers,
    ).json()


def test_approval_triggers_question_generation(client):
    _add_recruiter(client, "9812460001")
    recruiter_headers = _login(client, "9812460001")
    job = _make_job(client, recruiter_headers, ["Python", "SQL"])
    student_headers = _register_student(client, "9812460002")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python", "SQL"])

    workflow_before = client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=recruiter_headers
    ).json()
    stages_before = {s["key"]: s["state"] for s in workflow_before["stages"]}
    assert stages_before["interview"] == "pending"

    res = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    assert res.status_code == 200
    stages_after = {s["key"]: s["state"] for s in res.json()["stages"]}
    assert stages_after["interview"] == "completed"

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert len(detail["questions"]) == 4  # 2 skills + 2 generic
    categories = {q["category"] for q in detail["questions"]}
    assert "Python" in categories
    assert "SQL" in categories
    assert all(q["evaluation_criteria"] for q in detail["questions"])


def test_viewing_candidates_page_does_not_generate_questions(client):
    _add_recruiter(client, "9812460003")
    recruiter_headers = _login(client, "9812460003")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460004")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    client.get("/api/recruiters/me/candidates", headers=recruiter_headers)
    client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=recruiter_headers
    )

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert detail["questions"] == []
    assert detail["status_label"] == "Pending"


def test_approval_is_idempotent_and_does_not_duplicate_questions(client):
    _add_recruiter(client, "9812460005")
    recruiter_headers = _login(client, "9812460005")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460006")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert len(detail["questions"]) == 3  # 1 skill + 2 generic, not doubled


def test_schedule_interview_and_student_sees_invitation(client):
    _add_recruiter(client, "9812460007")
    recruiter_headers = _login(client, "9812460007")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460008")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )

    page = client.get("/api/recruiters/me/interviews", headers=recruiter_headers).json()
    assert len(page["eligible_candidates"]) == 1
    assert page["eligible_candidates"][0]["application_id"] == application["id"]

    res = client.post(
        f"/api/recruiters/me/interviews/{application['id']}/schedule",
        json={"interview_type": "Technical", "scheduled_at": "2026-10-01T10:00:00Z"},
        headers=recruiter_headers,
    )
    assert res.status_code == 200
    detail = res.json()
    assert detail["status_label"] == "Scheduled"
    assert detail["invitation_subject"] is not None
    assert "Backend Developer" in detail["invitation_body"]

    page_after = client.get("/api/recruiters/me/interviews", headers=recruiter_headers).json()
    assert page_after["summary"]["scheduled"] == 1
    assert page_after["eligible_candidates"] == []  # now scheduled, no longer eligible
    row = page_after["interviews"][0]
    assert row["status_label"] == "Scheduled"

    my_apps = client.get("/api/students/me/jobs/applications", headers=student_headers).json()
    assert my_apps[0]["status_label"] == "Interview Invitation"


def test_ai_status_and_interview_status_stay_separate(client):
    _add_recruiter(client, "9812460009")
    recruiter_headers = _login(client, "9812460009")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460010")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )
    client.post(
        f"/api/recruiters/me/interviews/{application['id']}/schedule",
        json={"interview_type": "Technical", "scheduled_at": "2026-10-01T10:00:00Z"},
        headers=recruiter_headers,
    )
    res = client.put(
        f"/api/recruiters/me/interviews/{application['id']}/status",
        json={"status": "completed"},
        headers=recruiter_headers,
    )
    assert res.status_code == 200
    detail = res.json()
    # Interview Status moved on to "Completed" while AI (question-generation)
    # Status independently stayed "Shortlisted"/"Hold"/etc — never merged.
    assert detail["status_label"] == "Completed"
    assert detail["ai_status_label"] in ("Shortlisted", "Hold", "Rejected")


def test_schedule_requires_eligibility(client):
    _add_recruiter(client, "9812460011")
    recruiter_headers = _login(client, "9812460011")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460012")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    # Not approved yet -> not eligible.
    res = client.post(
        f"/api/recruiters/me/interviews/{application['id']}/schedule",
        json={"interview_type": "Technical", "scheduled_at": "2026-10-01T10:00:00Z"},
        headers=recruiter_headers,
    )
    assert res.status_code == 400


def test_interviews_require_ownership_and_recruiter_role(client):
    _add_recruiter(client, "9812460013")
    _add_recruiter(client, "9812460014")
    headers_a = _login(client, "9812460013")
    headers_b = _login(client, "9812460014")

    job = _make_job(client, headers_a, ["Python"])
    student_headers = _register_student(client, "9812460015")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])
    client.post(f"/api/recruiters/me/candidates/{application['id']}/approve", headers=headers_a)

    res = client.get(f"/api/recruiters/me/interviews/{application['id']}", headers=headers_b)
    assert res.status_code == 404

    res = client.get("/api/recruiters/me/interviews", headers=student_headers)
    assert res.status_code == 403


def test_approval_resolves_profile_email_and_reports_transport_not_configured(client):
    """Recruiter Interview Invitation & Demo Email Specification §2/§5/§11:
    approval must actually resolve a real recipient email and attempt a
    send — this test environment has no EMAIL_HOST/EMAIL_USERNAME/
    EMAIL_PASSWORD/EMAIL_FROM configured, so the honest, correct outcome is
    a persisted "failed" status with a clear reason, never a fabricated
    "sent" tick."""
    _add_recruiter(client, "9812460016")
    recruiter_headers = _login(client, "9812460016")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460017")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert detail["recipient_email"] == "kavya@example.com"
    assert detail["email_source"] == "profile"
    assert detail["email_status"] == "failed"
    assert detail["email_status_label"] == "Failed"
    assert "not configured" in detail["email_error"].lower()

    workflow = client.get(
        f"/api/recruiters/me/candidates/{application['id']}/workflow", headers=recruiter_headers
    ).json()
    assert workflow["email_status"] == "failed"
    assert workflow["recipient_email"] == "kavya@example.com"
    stage_states = {s["key"]: s["state"] for s in workflow["stages"]}
    assert stage_states["email_invitation"] == "rejected"


def test_approval_sends_real_email_when_transport_is_configured(client):
    """When a demo SMTP mailbox actually is configured, approval must
    genuinely deliver the invitation through it and persist a real "sent"
    status — verified here via a mocked `smtplib.SMTP` standing in for the
    actual transport."""
    _add_recruiter(client, "9812460018")
    recruiter_headers = _login(client, "9812460018")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460019")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    from backend.core.config import settings

    with (
        patch.object(settings, "email_host", "smtp.example.com"),
        patch.object(settings, "email_username", "demo@example.com"),
        patch.object(settings, "email_password", "app-password"),
        patch.object(settings, "email_from", "demo@example.com"),
        patch("backend.services.email_service.smtplib.SMTP") as mock_smtp,
    ):
        mock_server = mock_smtp.return_value.__enter__.return_value
        client.post(
            f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
        )

        assert mock_server.login.called
        assert mock_server.send_message.called

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert detail["email_status"] == "sent"
    assert detail["email_status_label"] == "Sent"
    assert detail["email_sent_at_display"] is not None
    assert detail["email_error"] is None


def test_email_falls_back_to_resume_extracted_email_when_profile_email_missing(client):
    """Recruiter Interview Invitation & Demo Email Specification §5/§13:
    resume-extracted email is used only when the profile email is genuinely
    unavailable — never chosen arbitrarily."""
    _add_recruiter(client, "9812460020")
    recruiter_headers = _login(client, "9812460020")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460021")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    db = _db(client)
    from backend.models.student_profile import StudentProfile
    from backend.services.student_profile_service import apply_resume_extraction

    profile = db.query(StudentProfile).filter_by(full_name="Kavya Nair").one()
    profile.email = ""
    apply_resume_extraction(
        db, profile.student_id, "Skills\nPython\n\nContact: kavya.resume@example.com"
    )
    db.commit()

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert detail["recipient_email"] == "kavya.resume@example.com"
    assert detail["email_source"] == "resume"


def test_resume_re_extraction_does_not_clear_a_previously_found_email(client):
    """Email Invitation & Session Persistence Fix Specification §2: "must
    not replace an existing valid student email unnecessarily" — a later
    resume re-upload that doesn't itself state an email (e.g. a differently
    formatted resume, or an extraction that only partially succeeds) must
    not wipe out a previously found, still-valid resume-extracted email."""
    _add_recruiter(client, "9812460024")
    recruiter_headers = _login(client, "9812460024")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460025")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    db = _db(client)
    from backend.models.student_profile import StudentProfile
    from backend.services.student_profile_service import apply_resume_extraction

    profile = db.query(StudentProfile).filter_by(full_name="Kavya Nair").one()
    profile.email = ""
    db.commit()

    apply_resume_extraction(
        db, profile.student_id, "Skills\nPython\n\nContact: kavya.resume@example.com"
    )
    db.commit()

    # A later re-upload's text happens not to state an email this time.
    apply_resume_extraction(db, profile.student_id, "Skills\nPython, SQL")
    db.commit()

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert detail["recipient_email"] == "kavya.resume@example.com"
    assert detail["email_source"] == "resume"


def test_email_reports_unavailable_when_no_email_exists_anywhere(client):
    """§5 Case 3: neither a profile nor a resume email exists — the system
    must not invent one, and must report the recipient as unavailable."""
    _add_recruiter(client, "9812460022")
    recruiter_headers = _login(client, "9812460022")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460023")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    db = _db(client)
    from backend.models.student_profile import StudentProfile

    profile = db.query(StudentProfile).filter_by(full_name="Kavya Nair").one()
    profile.email = ""
    db.commit()

    client.post(
        f"/api/recruiters/me/candidates/{application['id']}/approve", headers=recruiter_headers
    )

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert detail["recipient_email"] is None
    assert detail["email_source"] == "unavailable"
    assert detail["email_status"] == "failed"
    assert "no valid recipient" in detail["email_error"].lower()


def test_disapproval_never_triggers_interview_or_email(client):
    """Persistent Authentication & Working Interview Invitation Email SDD
    §19: a recruiter's disapproval must never generate interview questions
    or attempt to send an invitation email — that entire workflow is
    approval-only, so a rejected candidate must show no trace of either."""
    _add_recruiter(client, "9812460026")
    recruiter_headers = _login(client, "9812460026")
    job = _make_job(client, recruiter_headers, ["Python"])
    student_headers = _register_student(client, "9812460027")
    application = _apply_with_skills(client, student_headers, job["id"], ["Python"])

    res = client.post(
        f"/api/recruiters/me/candidates/{application['id']}/disapprove",
        json={"reason": "Skill Gap: Python"},
        headers=recruiter_headers,
    )
    assert res.status_code == 200
    workflow = res.json()
    stage_states = {s["key"]: s["state"] for s in workflow["stages"]}
    assert stage_states["human_approval"] == "rejected"
    assert stage_states["interview"] == "pending"
    assert stage_states["email_invitation"] == "pending"
    assert workflow["interview_question_count"] == 0
    assert workflow["email_status"] is None
    assert workflow["recipient_email"] is None

    detail = client.get(
        f"/api/recruiters/me/interviews/{application['id']}", headers=recruiter_headers
    ).json()
    assert detail["questions"] == []
    assert detail["email_status"] == "pending"
    assert detail["recipient_email"] is None
