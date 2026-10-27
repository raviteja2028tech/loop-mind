"""Shared application status helpers — used by the Recruiter Dashboard
(Phase 11), Job Management (Phase 12), Candidates page (Phase 13), Human
Approval (Phase 14) and Interviews page (Phase 15) so they all agree on
what "shortlisted"/"under review"/"rejected" means for an application, how
to display a candidate's name, and how to look up an application scoped
to its owning recruiter.

`bucket()` is the Candidates page's own per-row, mutually-exclusive
human-decision status (Shortlisted = approved, Rejected = disapproved,
Under Review = no decision yet) — unchanged by the Recruiter Dashboard —
Final Specification. That spec's Dashboard summary cards use the three
functions below instead, which are deliberately *not* mutually exclusive:
`is_ai_shortlisted` reflects the Shortlisting Agent's own output
regardless of any later human decision, `is_awaiting_decision` is "no
recruiter decision yet" full stop (true from the moment an application is
created), and `is_recruiter_rejected` is a human disapproval specifically
(never the AI's own "rejected" recommendation, which a recruiter can
still override).
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.jobs import Job, JobApplication
from backend.models.student_profile import StudentProfessionalLinks, StudentProfile


class ApplicationNotFoundError(Exception):
    pass


def get_owned_application(db: Session, recruiter_id: int, application_id: int) -> JobApplication:
    """Raises `ApplicationNotFoundError` if the application doesn't exist
    or doesn't belong to one of this recruiter's own job postings —
    recruiter data isolation, enforced in one place."""
    application = db.scalar(select(JobApplication).where(JobApplication.id == application_id))
    if application is None or application.job.recruiter_id != recruiter_id:
        raise ApplicationNotFoundError(application_id)
    return application


def recruiter_applications(db: Session, recruiter_id: int) -> list[JobApplication]:
    job_ids = list(db.scalars(select(Job.id).where(Job.recruiter_id == recruiter_id)))
    if not job_ids:
        return []
    return list(
        db.scalars(
            select(JobApplication)
            .where(JobApplication.job_id.in_(job_ids))
            .order_by(JobApplication.applied_at.desc())
        )
    )


def bucket(application: JobApplication) -> str:
    """Returns "shortlisted" | "under_review" | "rejected" — the human
    decision (final) takes precedence over the AI match status (interim),
    which takes precedence over "under_review" (nothing has evaluated it
    yet)."""
    approval = application.approval
    if approval and approval.decision == "approved":
        return "shortlisted"
    if approval and approval.decision == "disapproved":
        return "rejected"
    match = application.match_result
    if match and match.ai_status == "shortlisted":
        return "shortlisted"
    if match and match.ai_status == "rejected":
        return "rejected"
    return "under_review"


def is_ai_shortlisted(application: JobApplication) -> bool:
    """Recruiter Dashboard — Final Specification §1: the Dashboard's
    "Shortlisted" card is based on the Shortlisting Agent's own output
    specifically — never on skills, never on whether a recruiter has
    since made a decision. Deliberately independent of, and can overlap
    with, `is_awaiting_decision` below (an AI-shortlisted application the
    recruiter hasn't decided on yet is both Shortlisted *and* Under
    Review at once — the two are no longer mutually exclusive)."""
    match = application.match_result
    return bool(match and match.ai_status == "shortlisted")


def is_awaiting_decision(application: JobApplication) -> bool:
    """Recruiter Dashboard — Final Specification §1/§3/§10: "Under
    Review" — an application that has reached (or is waiting to reach)
    the Human-in-the-Loop stage and has no recruiter decision yet, full
    stop. A brand new application is Under Review the moment it's
    created, before the Shortlisting Agent has even run (§10's "when a
    new application arrives: Total Applications +1, Under Review +1") —
    this is not the same question as "has the AI shortlisted it."""
    return application.approval is None


def is_recruiter_rejected(application: JobApplication) -> bool:
    """Recruiter Dashboard — Final Specification §2: "Rejected" means a
    *recruiter's* Human-in-the-Loop disapproval specifically — never the
    Shortlisting Agent's own "rejected" AI status, which is a separate,
    interim recommendation a recruiter can still override either way."""
    approval = application.approval
    return bool(approval and approval.decision == "disapproved")


def ai_status_label(application: JobApplication) -> str:
    match = application.match_result
    if match and match.ai_status:
        return match.ai_status.replace("_", " ").title()
    return "Pending"


def candidate_name(db: Session, student_id: int) -> str:
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    return profile.full_name if profile and profile.full_name else "Student"


def resolve_recipient_email(db: Session, student_id: int) -> tuple[str | None, str]:
    """Recruiter Interview Invitation & Demo Email Specification §5/§13:
    the fixed priority order for an interview invitation's recipient —
    the student's own profile email, then (only if that's unavailable) the
    email the Resume Parser Agent found in their uploaded resume. Never
    invents an address: returns (None, "unavailable") when neither exists.
    Source is reported alongside the address so callers can be transparent
    about which one was actually used, rather than picking one silently."""
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    if profile and profile.email:
        return profile.email, "profile"

    links = db.scalar(
        select(StudentProfessionalLinks).where(StudentProfessionalLinks.student_id == student_id)
    )
    if links and links.resume_extracted_email:
        return links.resume_extracted_email, "resume"

    return None, "unavailable"
