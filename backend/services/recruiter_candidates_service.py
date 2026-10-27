"""Recruiter Candidates Page — phase.md Phase 13.

Candidates originate from real job applications (spec.md §11): "Recruiter
creates Job -> Job available in Student Portal -> Student applies ->
Application created -> Candidate appears in Recruiter Candidates." This
module reads those same `JobApplication` rows, auto-running the AI
recruitment pipeline (backend/services/recruitment_ai_service.py) for any
application that hasn't been evaluated yet — matching the established
auto-run-on-view pattern from the Skill Gap page (Phase 08).

`approve_candidate`/`disapprove_candidate` are phase.md Phase 14 (Human
Approval & Recruitment Outcome) — the mandatory recruiter cross-check.
The AI status (Shortlisting Agent) and the human decision recorded here
are deliberately kept as two separate fields (`AIMatchResult.ai_status` vs
`HumanApproval.decision`) so one never silently overwrites the other.
Approval also triggers the Interview Agent (Phase 15) — spec.md's own
boundary: question generation happens "through the previously defined
recruitment workflow," not merely because someone opens a page.
"""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.jobs import HumanApproval, Job, JobApplication
from backend.schemas.recruiter_candidates import (
    CandidateFilterOptionsOut,
    CandidateRowOut,
    CandidatesPageOut,
    CandidateSummaryOut,
    CandidateWorkflowOut,
    JobOptionOut,
    SelectedCandidateOut,
    WorkflowStageOut,
)
from backend.services import interview_service, recruitment_ai_service
from backend.services.application_status import (
    ai_status_label,
    bucket,
    candidate_name,
    get_owned_application,
    recruiter_applications,
)
from backend.services.interview_service import EMAIL_STATUS_LABEL
from backend.services.time_format import relative_time

_BUCKET_LABEL = {
    "shortlisted": "Shortlisted",
    "under_review": "Under Review",
    "rejected": "Rejected",
}

_STAGE_DEFS = [
    ("resume_parser", "Resume Parser"),
    ("embedding", "Embedding"),
    ("matching", "Matching"),
    ("shortlisting", "Shortlisting"),
    ("human_approval", "Human Approval"),
    ("interview", "Interview"),
    ("email_invitation", "Email Invitation"),
]


def _to_row(db: Session, application: JobApplication) -> CandidateRowOut:
    match = application.match_result
    return CandidateRowOut(
        application_id=application.id,
        candidate_name=candidate_name(db, application.student_id),
        job_id=application.job_id,
        job_title=application.job.job_title,
        applied_role=application.job.job_role,
        applied_relative=relative_time(application.applied_at),
        ai_score=match.ai_score if match else None,
        matching_factors=(
            match.matching_factors.get("matching_factors")
            if match and match.matching_factors
            else None
        ),
        status_label=_BUCKET_LABEL[bucket(application)],
        ai_evaluation_label=ai_status_label(application),
    )


def _matches_search(db: Session, application: JobApplication, needle: str) -> bool:
    if needle in candidate_name(db, application.student_id).lower():
        return True
    if needle in application.job.job_role.lower():
        return True
    if application.match_result and application.match_result.matching_factors:
        matched_skills = application.match_result.matching_factors.get("matched_skills", [])
        if any(needle in skill.lower() for skill in matched_skills):
            return True
    return False


def get_candidates_page(
    db: Session,
    recruiter_id: int,
    *,
    search: str | None = None,
    job_id: int | None = None,
    status: str | None = None,
    ai_evaluation: str | None = None,
) -> CandidatesPageOut:
    applications = recruiter_applications(db, recruiter_id)

    # Auto-evaluate any application the recruiter hasn't seen before this
    # page load — spec.md: "When an application is received, the AI
    # recruitment workflow first processes the candidate's resume."
    for application in applications:
        recruitment_ai_service.ensure_match_result(db, application)

    total_candidates = len(applications)
    buckets = {a.id: bucket(a) for a in applications}
    shortlisted = sum(1 for b in buckets.values() if b == "shortlisted")
    rejected = sum(1 for b in buckets.values() if b == "rejected")
    under_review = total_candidates - shortlisted - rejected

    jobs = list(db.scalars(select(Job).where(Job.recruiter_id == recruiter_id)))
    filters = CandidateFilterOptionsOut(
        jobs=[JobOptionOut(id=j.id, job_title=j.job_title) for j in jobs],
        statuses=["Shortlisted", "Under Review", "Rejected"],
        ai_evaluations=["Shortlisted", "Hold", "Rejected"],
    )

    rows = applications
    if job_id is not None:
        rows = [a for a in rows if a.job_id == job_id]
    if status:
        rows = [a for a in rows if _BUCKET_LABEL[bucket(a)] == status]
    if ai_evaluation:
        rows = [a for a in rows if ai_status_label(a) == ai_evaluation]
    if search:
        needle = search.strip().lower()
        if needle:
            rows = [a for a in rows if _matches_search(db, a, needle)]

    return CandidatesPageOut(
        summary=CandidateSummaryOut(
            total_candidates=total_candidates,
            shortlisted=shortlisted,
            under_review=under_review,
            rejected=rejected,
        ),
        filters=filters,
        candidates=[_to_row(db, a) for a in rows],
    )


def get_workflow(db: Session, recruiter_id: int, application_id: int) -> CandidateWorkflowOut:
    application = get_owned_application(db, recruiter_id, application_id)
    match = recruitment_ai_service.ensure_match_result(db, application)

    factors = match.matching_factors or {}
    matched_skills = factors.get("matched_skills", [])
    missing_skills = factors.get("missing_skills", [])

    approval = application.approval
    if approval and approval.decision == "approved":
        human_approval_state = "approved"
    elif approval and approval.decision == "disapproved":
        human_approval_state = "rejected"
    else:
        human_approval_state = "pending"

    interview = application.interview
    if interview and interview.ai_question_status == "generated":
        interview_state = "completed"
    elif interview and interview.ai_question_status == "generating":
        interview_state = "running"
    else:
        interview_state = "pending"

    # Email Invitation (Recruiter Interview Invitation & Demo Email
    # Specification §11): reflects the real, persisted send outcome —
    # never inferred from scheduling — so a failed send is visibly
    # distinct from one that hasn't been attempted yet.
    if interview and interview.email_status == "sent":
        email_state = "completed"
    elif interview and interview.email_status == "sending":
        email_state = "running"
    elif interview and interview.email_status == "failed":
        email_state = "rejected"
    else:
        email_state = "pending"

    stage_states = {
        "resume_parser": "completed",
        "embedding": "completed",
        "matching": "completed",
        "shortlisting": "completed",
        "human_approval": human_approval_state,
        "interview": interview_state,
        "email_invitation": email_state,
    }
    stages = [
        WorkflowStageOut(key=key, label=label, state=stage_states[key])
        for key, label in _STAGE_DEFS
    ]

    return CandidateWorkflowOut(
        selected_candidate=SelectedCandidateOut(
            candidate_name=candidate_name(db, application.student_id),
            applied_role=application.job.job_role,
            ai_score=match.ai_score,
        ),
        stages=stages,
        matching_factors=factors.get("matching_factors"),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        human_decision=approval.decision if approval else None,
        disapproval_reason=approval.reason
        if approval and approval.decision == "disapproved"
        else None,
        interview_question_count=len(interview.questions) if interview else 0,
        email_status=interview.email_status if interview else None,
        email_status_label=EMAIL_STATUS_LABEL.get(interview.email_status) if interview else None,
        recipient_email=interview.recipient_email if interview else None,
        email_source=interview.email_source if interview else None,
        email_error=interview.email_error if interview else None,
        historical_signal=factors.get("historical_signal"),
    )


def _get_or_create_approval(db: Session, application: JobApplication) -> HumanApproval:
    if application.approval is not None:
        return application.approval
    approval = HumanApproval(application_id=application.id)
    db.add(approval)
    return approval


def approve_candidate(db: Session, recruiter_id: int, application_id: int) -> CandidateWorkflowOut:
    application = get_owned_application(db, recruiter_id, application_id)
    approval = _get_or_create_approval(db, application)
    approval.decision = "approved"
    approval.reason = None
    approval.decided_at = datetime.now(UTC)
    db.commit()
    # spec.md's boundary: question generation happens "through the
    # previously defined recruitment workflow" — i.e. triggered by this
    # approval event, never merely by the recruiter viewing a page.
    interview = interview_service.generate_questions_for_approval(db, application)
    # Recruiter Interview Invitation & Demo Email Specification §2: the
    # Email Agent runs immediately after the Interview Agent within this
    # same approval event, not on a later page view or a separate
    # scheduling action.
    if interview.ai_question_status == "generated":
        interview_service.send_invitation_email(db, application, interview)
    return get_workflow(db, recruiter_id, application_id)


def disapprove_candidate(
    db: Session, recruiter_id: int, application_id: int, reason: str
) -> CandidateWorkflowOut:
    application = get_owned_application(db, recruiter_id, application_id)
    approval = _get_or_create_approval(db, application)
    approval.decision = "disapproved"
    approval.reason = reason
    approval.decided_at = datetime.now(UTC)
    db.commit()
    return get_workflow(db, recruiter_id, application_id)
