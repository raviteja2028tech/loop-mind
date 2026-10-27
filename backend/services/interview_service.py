"""Recruiter Interviews Page & Interview/Email Agents — phase.md Phase 15.

spec.md's boundary: interview question generation is triggered by the
recruiter-approval event (Phase 14's `approve_candidate`), never merely by
viewing the Interviews page — unlike Phase 13's AI-matching, which IS
auto-run-on-view. `generate_questions_for_approval` is the one entry point
that starts question generation, called from
`recruiter_candidates_service.approve_candidate`.

AI Status (`Interview.ai_question_status`: not_started/generating/generated)
and Interview Status (`Interview.status`: pending/scheduled/completed/
cancelled) are deliberately separate columns (spec.md §17) and are never
merged into one field here.
"""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.ai_bridge import ensure_ai_services_importable
from backend.models.jobs import Interview, InterviewQuestion, Job, JobApplication
from backend.schemas.recruiter_candidates import JobOptionOut
from backend.schemas.recruiter_dashboard import RecentActivityItemOut
from backend.schemas.recruiter_interviews import (
    EligibleCandidateOut,
    InterviewDetailOut,
    InterviewFilterOptionsOut,
    InterviewRowOut,
    InterviewsPageOut,
    InterviewSummaryOut,
    QuestionOut,
)
from backend.services import email_service
from backend.services.application_status import (
    ai_status_label,
    candidate_name,
    get_owned_application,
    recruiter_applications,
    resolve_recipient_email,
)
from backend.services.time_format import relative_time

ensure_ai_services_importable()

from agents.email_agent import EmailAgent  # noqa: E402
from agents.interview_agent import InterviewAgent  # noqa: E402

_interview_agent = InterviewAgent()
_email_agent = EmailAgent()

_STATUS_LABEL = {
    "pending": "Pending",
    "scheduled": "Scheduled",
    "completed": "Completed",
    "cancelled": "Cancelled",
}

_OUTCOME_LABEL = {
    "hired": "Hired",
    "not_selected": "Not Selected",
}

EMAIL_STATUS_LABEL = {
    "pending": "Pending",
    "sending": "Sending",
    "sent": "Sent",
    "failed": "Failed",
}


def _get_or_create_interview(db: Session, application: JobApplication) -> Interview:
    if application.interview is not None:
        return application.interview
    interview = Interview(application_id=application.id)
    db.add(interview)
    return interview


def generate_questions_for_approval(db: Session, application: JobApplication) -> Interview:
    """Idempotent — a candidate already approved once (re-approval, or a
    second view) never regenerates questions or duplicates rows."""
    interview = _get_or_create_interview(db, application)
    if interview.ai_question_status == "generated":
        return interview

    interview.ai_question_status = "generating"
    db.flush()

    questions = _interview_agent.run(application.job.job_role, application.job.required_skills)
    for q in questions:
        db.add(
            InterviewQuestion(
                interview_id=interview.id,
                question_text=q["question_text"],
                category=q["category"],
                evaluation_criteria=q["evaluation_criteria"],
            )
        )
    interview.ai_question_status = "generated"
    db.commit()
    db.refresh(interview)
    return interview


def _interview_details_summary(interview: Interview) -> tuple[str, str]:
    """Recruiter Interview Invitation & Demo Email Specification §9: the
    invitation's "Interview Details" content must be actual stored data,
    never a fabricated schedule. At approval time the interview usually
    hasn't been scheduled yet (that's a separate recruiter action), so this
    honestly states the real, current process state instead of inventing a
    type/time — once `schedule_interview` sets real values, later views of
    the invitation (`get_interview_detail`) already show those instead."""
    interview_type = interview.interview_type or "To be determined"
    if interview.scheduled_at:
        scheduled_at_display = interview.scheduled_at.strftime("%b %d, %Y · %I:%M %p")
    else:
        scheduled_at_display = (
            "to be scheduled — you will be contacted separately with the exact date and time"
        )
    return interview_type, scheduled_at_display


def send_invitation_email(
    db: Session, application: JobApplication, interview: Interview
) -> Interview:
    """Recruiter Interview Invitation & Demo Email Specification §2/§4-5:
    runs immediately after question generation, resolving the student's
    real recipient email (profile first, then resume-parsed — never
    invented), composing an application-specific invitation from the
    actual job/company/matched-skill data, and attempting a real send
    through the configured demo SMTP transport. Idempotent — once a send
    has reached a terminal "sent" state, re-approving the same application
    never re-sends or duplicates anything; a "failed" attempt does allow
    another attempt on the next approval, since nothing was ever
    successfully delivered the first time."""
    if interview.email_status == "sent":
        return interview

    recipient, source = resolve_recipient_email(db, application.student_id)
    interview.recipient_email = recipient
    interview.email_source = source

    if recipient is None:
        interview.email_status = "failed"
        interview.email_error = "No valid recipient email is available for this candidate."
        db.commit()
        db.refresh(interview)
        return interview

    interview.email_status = "sending"
    db.commit()

    match = application.match_result
    matched_skills = (
        match.matching_factors.get("matched_skills", []) if match and match.matching_factors else []
    )
    interview_type, scheduled_at_display = _interview_details_summary(interview)

    invitation = _email_agent.generate_interview_invitation(
        candidate_name=candidate_name(db, application.student_id),
        job_title=application.job.job_title,
        job_role=application.job.job_role,
        company_name=application.job.company_name,
        interview_type=interview_type,
        scheduled_at_display=scheduled_at_display,
        matched_skills=matched_skills,
    )

    sent, message = email_service.send_email(
        to_address=recipient, subject=invitation["subject"], body=invitation["body"]
    )
    interview.email_status = "sent" if sent else "failed"
    interview.email_sent_at = datetime.now(UTC) if sent else None
    interview.email_error = None if sent else message
    db.commit()
    db.refresh(interview)
    return interview


def _eligible(application: JobApplication) -> bool:
    """Eligible for scheduling: the recruiter has approved the candidate
    and question generation has completed."""
    approval = application.approval
    interview = application.interview
    return bool(
        approval
        and approval.decision == "approved"
        and interview
        and interview.ai_question_status == "generated"
    )


def get_interviews_page(db: Session, recruiter_id: int) -> InterviewsPageOut:
    applications = recruiter_applications(db, recruiter_id)

    scheduled_rows = [a for a in applications if a.interview and a.interview.status != "pending"]
    total_interviews = len(scheduled_rows)
    scheduled = sum(1 for a in scheduled_rows if a.interview.status == "scheduled")
    completed = sum(1 for a in scheduled_rows if a.interview.status == "completed")
    cancelled = sum(1 for a in scheduled_rows if a.interview.status == "cancelled")

    jobs = list(db.scalars(select(Job).where(Job.recruiter_id == recruiter_id)))
    filters = InterviewFilterOptionsOut(
        jobs=[JobOptionOut(id=j.id, job_title=j.job_title) for j in jobs],
        statuses=["Scheduled", "Completed", "Cancelled"],
    )

    interview_rows = [
        InterviewRowOut(
            application_id=a.id,
            candidate_name=candidate_name(db, a.student_id),
            job_id=a.job_id,
            job_role=a.job.job_role,
            interview_type=a.interview.interview_type,
            scheduled_at=a.interview.scheduled_at,
            scheduled_at_display=(
                a.interview.scheduled_at.strftime("%b %d, %Y · %I:%M %p")
                if a.interview.scheduled_at
                else None
            ),
            ai_status_label=ai_status_label(a),
            status_label=_STATUS_LABEL[a.interview.status],
            outcome_label=_OUTCOME_LABEL.get(a.interview.outcome),
        )
        for a in sorted(scheduled_rows, key=lambda a: a.interview.created_at, reverse=True)
    ]

    eligible_candidates = [
        EligibleCandidateOut(
            application_id=a.id,
            candidate_name=candidate_name(db, a.student_id),
            job_role=a.job.job_role,
        )
        for a in applications
        if _eligible(a) and (a.interview is None or a.interview.status == "pending")
    ]

    activity_events: list[tuple[datetime, RecentActivityItemOut]] = []
    for a in applications:
        interview = a.interview
        if interview is None:
            continue
        if interview.ai_question_status == "generated":
            activity_events.append(
                (
                    interview.created_at,
                    RecentActivityItemOut(
                        label="Interview questions generated",
                        detail=f"{candidate_name(db, a.student_id)} — {a.job.job_role}",
                        relative_time=relative_time(interview.created_at),
                    ),
                )
            )
        if interview.status in ("scheduled", "completed", "cancelled"):
            label = {
                "scheduled": "Interview scheduled",
                "completed": "Interview completed",
                "cancelled": "Interview cancelled",
            }[interview.status]
            activity_events.append(
                (
                    interview.updated_at,
                    RecentActivityItemOut(
                        label=label,
                        detail=f"{candidate_name(db, a.student_id)} — {a.job.job_role}",
                        relative_time=relative_time(interview.updated_at),
                    ),
                )
            )
        if interview.outcome:
            activity_events.append(
                (
                    interview.updated_at,
                    RecentActivityItemOut(
                        label=f"Recruitment outcome recorded: {_OUTCOME_LABEL[interview.outcome]}",
                        detail=f"{candidate_name(db, a.student_id)} — {a.job.job_role}",
                        relative_time=relative_time(interview.updated_at),
                    ),
                )
            )
    activity_events.sort(key=lambda pair: pair[0], reverse=True)
    recent_activity = [item for _, item in activity_events[:5]]

    return InterviewsPageOut(
        summary=InterviewSummaryOut(
            total_interviews=total_interviews,
            scheduled=scheduled,
            completed=completed,
            cancelled=cancelled,
        ),
        filters=filters,
        interviews=interview_rows,
        eligible_candidates=eligible_candidates,
        recent_activity=recent_activity,
    )


def get_interview_detail(db: Session, recruiter_id: int, application_id: int) -> InterviewDetailOut:
    application = get_owned_application(db, recruiter_id, application_id)
    interview = application.interview

    match = application.match_result
    missing_skills = (
        match.matching_factors.get("missing_skills", []) if match and match.matching_factors else []
    )
    matched_skills = (
        match.matching_factors.get("matched_skills", []) if match and match.matching_factors else []
    )

    questions = (
        [
            QuestionOut(
                question_text=q.question_text,
                category=q.category,
                evaluation_criteria=q.evaluation_criteria,
            )
            for q in interview.questions
        ]
        if interview
        else []
    )

    invitation_subject = None
    invitation_body = None
    if interview and interview.scheduled_at:
        invitation = _email_agent.generate_interview_invitation(
            candidate_name=candidate_name(db, application.student_id),
            job_title=application.job.job_title,
            job_role=application.job.job_role,
            company_name=application.job.company_name,
            interview_type=interview.interview_type or "Technical",
            scheduled_at_display=interview.scheduled_at.strftime("%b %d, %Y · %I:%M %p"),
            matched_skills=matched_skills,
        )
        invitation_subject = invitation["subject"]
        invitation_body = invitation["body"]

    return InterviewDetailOut(
        candidate_name=candidate_name(db, application.student_id),
        job_role=application.job.job_role,
        interview_type=interview.interview_type if interview else None,
        scheduled_at_display=(
            interview.scheduled_at.strftime("%b %d, %Y · %I:%M %p")
            if interview and interview.scheduled_at
            else None
        ),
        ai_status_label=ai_status_label(application),
        status_label=_STATUS_LABEL[interview.status] if interview else "Pending",
        questions=questions,
        invitation_subject=invitation_subject,
        invitation_body=invitation_body,
        missing_skills=missing_skills,
        outcome=interview.outcome if interview else None,
        outcome_label=_OUTCOME_LABEL.get(interview.outcome) if interview else None,
        outcome_reason=interview.outcome_reason if interview else None,
        email_status=interview.email_status if interview else "pending",
        email_status_label=EMAIL_STATUS_LABEL[interview.email_status if interview else "pending"],
        recipient_email=interview.recipient_email if interview else None,
        email_source=interview.email_source if interview else None,
        email_sent_at_display=(
            interview.email_sent_at.strftime("%b %d, %Y · %I:%M %p")
            if interview and interview.email_sent_at
            else None
        ),
        email_error=interview.email_error if interview else None,
    )


class InterviewNotEligibleError(Exception):
    pass


class InterviewNotCompletedError(Exception):
    pass


def schedule_interview(
    db: Session,
    recruiter_id: int,
    application_id: int,
    *,
    interview_type: str,
    scheduled_at: datetime,
) -> InterviewDetailOut:
    application = get_owned_application(db, recruiter_id, application_id)
    if not _eligible(application):
        raise InterviewNotEligibleError(application_id)

    interview = application.interview
    interview.interview_type = interview_type
    interview.scheduled_at = scheduled_at
    interview.status = "scheduled"
    db.commit()
    return get_interview_detail(db, recruiter_id, application_id)


def set_interview_status(
    db: Session, recruiter_id: int, application_id: int, status_value: str
) -> InterviewDetailOut:
    application = get_owned_application(db, recruiter_id, application_id)
    interview = application.interview
    if interview is None:
        raise InterviewNotEligibleError(application_id)
    interview.status = status_value
    db.commit()
    return get_interview_detail(db, recruiter_id, application_id)


def set_interview_outcome(
    db: Session,
    recruiter_id: int,
    application_id: int,
    *,
    outcome: str,
    reason: str | None,
) -> InterviewDetailOut:
    """phase.md Phase 16: the "Outcome" node of the closed loop — only
    recordable once the interview has actually happened, and only here:
    never inferred automatically from a status change."""
    application = get_owned_application(db, recruiter_id, application_id)
    interview = application.interview
    if interview is None or interview.status != "completed":
        raise InterviewNotCompletedError(application_id)
    interview.outcome = outcome
    interview.outcome_reason = reason if outcome == "not_selected" else None
    db.commit()
    return get_interview_detail(db, recruiter_id, application_id)
