"""Student Jobs & Application System — phase.md Phase 10.

Job *creation* is now a Recruiter Portal feature (Phase 12,
backend/services/recruiter_jobs_service.py); this module only reads the
Job dataset (seeded or recruiter-created) and manages a student's own
saved jobs and applications against it.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.jobs import Job, JobApplication, SavedJob
from backend.models.student_profile import StudentProfessionalLinks, StudentProfile
from backend.schemas.jobs import (
    ApplicationOut,
    ApplyValidationOut,
    FilterOptionsOut,
    JobCardOut,
    JobSummaryOut,
    MissingRequirementOut,
)
from backend.services.time_format import relative_posted


class JobNotFoundError(Exception):
    pass


def list_filter_options(db: Session) -> FilterOptionsOut:
    jobs = list(db.scalars(select(Job).where(Job.status == "active")))
    return FilterOptionsOut(
        companies=sorted({j.company_name for j in jobs}),
        job_roles=sorted({j.job_role for j in jobs}),
        locations=sorted({j.location for j in jobs if j.location}),
        job_types=sorted({j.job_type for j in jobs if j.job_type}),
        experience_levels=sorted({j.experience_required for j in jobs}),
    )


def get_summary(db: Session, student_id: int) -> JobSummaryOut:
    total_jobs = len(list(db.scalars(select(Job.id).where(Job.status == "active"))))
    applications = list(
        db.scalars(select(JobApplication).where(JobApplication.student_id == student_id))
    )
    applied = len(applications)
    shortlisted = 0
    disapproved = 0
    for application in applications:
        approval = application.approval
        if approval and approval.decision == "approved":
            shortlisted += 1
        elif approval and approval.decision == "disapproved":
            disapproved += 1
    under_review = applied - shortlisted - disapproved
    return JobSummaryOut(
        total_jobs=total_jobs,
        applied=applied,
        under_review=under_review,
        shortlisted=shortlisted,
    )


def _to_card(job: Job, saved_ids: set[int], applied_ids: set[int]) -> JobCardOut:
    return JobCardOut(
        id=job.id,
        company_name=job.company_name,
        job_title=job.job_title,
        job_role=job.job_role,
        location=job.location,
        job_type=job.job_type,
        work_mode=job.work_mode,
        experience_required=job.experience_required,
        description=job.description,
        required_skills=job.required_skills,
        status="Open" if job.status == "active" else "Closed",
        posted_relative=relative_posted(job.created_at),
        is_saved=job.id in saved_ids,
        has_applied=job.id in applied_ids,
    )


def list_jobs(
    db: Session,
    student_id: int,
    *,
    search: str | None = None,
    companies: list[str] | None = None,
    job_roles: list[str] | None = None,
    locations: list[str] | None = None,
    job_types: list[str] | None = None,
    experience_levels: list[str] | None = None,
) -> list[JobCardOut]:
    query = select(Job).where(Job.status == "active")
    if companies:
        query = query.where(Job.company_name.in_(companies))
    if job_roles:
        query = query.where(Job.job_role.in_(job_roles))
    if locations:
        query = query.where(Job.location.in_(locations))
    if job_types:
        query = query.where(Job.job_type.in_(job_types))
    if experience_levels:
        query = query.where(Job.experience_required.in_(experience_levels))

    jobs = list(db.scalars(query.order_by(Job.created_at.desc())))

    if search:
        needle = search.strip().lower()
        if needle:
            jobs = [
                j
                for j in jobs
                if needle in j.company_name.lower()
                or needle in j.job_role.lower()
                or needle in j.job_title.lower()
                or any(needle in skill.lower() for skill in j.required_skills)
            ]

    saved_ids = {
        sj.job_id for sj in db.scalars(select(SavedJob).where(SavedJob.student_id == student_id))
    }
    applied_ids = {
        a.job_id
        for a in db.scalars(select(JobApplication).where(JobApplication.student_id == student_id))
    }
    return [_to_card(j, saved_ids, applied_ids) for j in jobs]


def toggle_saved(db: Session, student_id: int, job_id: int) -> bool:
    """Returns the new saved state."""
    if db.scalar(select(Job.id).where(Job.id == job_id)) is None:
        raise JobNotFoundError(job_id)
    existing = db.scalar(
        select(SavedJob).where(SavedJob.student_id == student_id, SavedJob.job_id == job_id)
    )
    if existing:
        db.delete(existing)
        db.commit()
        return False
    db.add(SavedJob(student_id=student_id, job_id=job_id))
    db.commit()
    return True


def validate_application_requirements(db: Session, student_id: int) -> ApplyValidationOut:
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    links = db.scalar(
        select(StudentProfessionalLinks).where(StudentProfessionalLinks.student_id == student_id)
    )
    missing: list[MissingRequirementOut] = []
    if not profile or not profile.full_name:
        missing.append(
            MissingRequirementOut(
                field="full_name",
                label="Full Name",
                reason="Your full name is required to apply for this job.",
            )
        )
    if not profile or not profile.email:
        missing.append(
            MissingRequirementOut(
                field="email",
                label="Email",
                reason="Your email is required to apply for this job.",
            )
        )
    if not links or not links.resume_file_path:
        missing.append(
            MissingRequirementOut(
                field="resume",
                label="Resume",
                reason=(
                    "Your resume is required to apply for this job. "
                    "Please upload your resume to continue."
                ),
            )
        )
    return ApplyValidationOut(can_apply=len(missing) == 0, missing=missing)


def _status_label(application: JobApplication) -> tuple[str, str | None]:
    approval = application.approval
    interview = application.interview
    # Recruitment Outcome (phase.md Phase 16) is the final word once the
    # interview has actually happened — it supersedes every earlier label.
    if interview and interview.outcome == "hired":
        return "Hired", None
    if interview and interview.outcome == "not_selected":
        return "Not Selected", interview.outcome_reason
    if approval and approval.decision == "disapproved":
        return "Disapproved", approval.reason
    if interview and interview.scheduled_at and interview.status == "scheduled":
        return "Interview Invitation", None
    if approval and approval.decision == "approved":
        return "Shortlisted", None
    return "Under Review", None


def _to_application_out(application: JobApplication) -> ApplicationOut:
    status_label, reason = _status_label(application)
    return ApplicationOut(
        id=application.id,
        job_id=application.job_id,
        job_title=application.job.job_title,
        company_name=application.job.company_name,
        job_role=application.job.job_role,
        status_label=status_label,
        disapproval_reason=reason,
        applied_at=application.applied_at,
    )


def apply_to_job(db: Session, student_id: int, job_id: int) -> ApplicationOut | ApplyValidationOut:
    """Returns the created/existing ApplicationOut on success, or the
    ApplyValidationOut (with `can_apply=False`) if required information is
    missing — the caller distinguishes by type."""
    job = db.scalar(select(Job).where(Job.id == job_id))
    if job is None:
        raise JobNotFoundError(job_id)

    existing = db.scalar(
        select(JobApplication).where(
            JobApplication.student_id == student_id, JobApplication.job_id == job_id
        )
    )
    if existing:
        return _to_application_out(existing)

    validation = validate_application_requirements(db, student_id)
    if not validation.can_apply:
        return validation

    links = db.scalar(
        select(StudentProfessionalLinks).where(StudentProfessionalLinks.student_id == student_id)
    )
    application = JobApplication(
        job_id=job_id,
        student_id=student_id,
        resume_snapshot_path=links.resume_file_path if links else None,
        status="applied",
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return _to_application_out(application)


def list_my_applications(db: Session, student_id: int) -> list[ApplicationOut]:
    applications = list(
        db.scalars(
            select(JobApplication)
            .where(JobApplication.student_id == student_id)
            .order_by(JobApplication.applied_at.desc())
        )
    )
    return [_to_application_out(a) for a in applications]
