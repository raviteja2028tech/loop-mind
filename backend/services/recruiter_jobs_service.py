"""Recruiter Job Management & Create New Job — phase.md Phase 12.

spec.md: "The recruiter creates the job once. The same stored job record
must be used by both portals" — this module writes to the exact same
`Job` table backend/services/jobs_service.py (Student Jobs, Phase 10)
reads from, so a newly created job is immediately visible to students
with no separate sync step.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.jobs import Job, JobApplication
from backend.schemas.recruiter_jobs import (
    JobCreateIn,
    RecruiterJobRowOut,
    RecruiterJobsPageOut,
    RecruiterJobsSummaryOut,
)
from backend.services.application_status import bucket
from backend.services.time_format import relative_posted


class JobNotFoundError(Exception):
    pass


def _to_row(job: Job, applications: list[JobApplication]) -> RecruiterJobRowOut:
    shortlisted = sum(1 for a in applications if bucket(a) == "shortlisted")
    rejected = sum(1 for a in applications if bucket(a) == "rejected")
    return RecruiterJobRowOut(
        id=job.id,
        company_name=job.company_name,
        job_title=job.job_title,
        job_role=job.job_role,
        experience_required=job.experience_required,
        location=job.location,
        job_type=job.job_type,
        work_mode=job.work_mode,
        description=job.description,
        required_skills=job.required_skills,
        applications=len(applications),
        shortlisted=shortlisted,
        under_review=len(applications) - shortlisted - rejected,
        rejected=rejected,
        status="Active" if job.status == "active" else "Paused",
        posted_relative=relative_posted(job.created_at),
        created_at=job.created_at,
    )


def get_jobs_page(
    db: Session,
    recruiter_id: int,
    *,
    search: str | None = None,
    status: str | None = None,
) -> RecruiterJobsPageOut:
    all_jobs = list(db.scalars(select(Job).where(Job.recruiter_id == recruiter_id)))
    total_jobs = len(all_jobs)
    active_jobs = sum(1 for j in all_jobs if j.status == "active")

    all_applications = (
        list(
            db.scalars(
                select(JobApplication).where(JobApplication.job_id.in_([j.id for j in all_jobs]))
            )
        )
        if all_jobs
        else []
    )

    jobs = all_jobs
    if status and status != "all":
        jobs = [j for j in jobs if j.status == status]
    if search:
        needle = search.strip().lower()
        if needle:
            jobs = [
                j
                for j in jobs
                if needle in j.job_title.lower()
                or needle in j.job_role.lower()
                or any(needle in skill.lower() for skill in j.required_skills)
            ]
    jobs.sort(key=lambda j: j.created_at, reverse=True)

    rows = [_to_row(job, [a for a in all_applications if a.job_id == job.id]) for job in jobs]

    return RecruiterJobsPageOut(
        summary=RecruiterJobsSummaryOut(
            total_jobs=total_jobs,
            active_jobs=active_jobs,
            paused_jobs=total_jobs - active_jobs,
            total_applications=len(all_applications),
        ),
        jobs=rows,
    )


def create_job(db: Session, recruiter_id: int, data: JobCreateIn) -> RecruiterJobRowOut:
    job = Job(
        recruiter_id=recruiter_id,
        company_name=data.company_name,
        job_title=data.job_title,
        job_role=data.job_role,
        experience_required=data.experience_required,
        required_skills=data.required_skills,
        job_type=data.job_type,
        work_mode=data.work_mode,
        location=data.location,
        description=data.description,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return _to_row(job, [])


def _get_owned_job(db: Session, recruiter_id: int, job_id: int) -> Job:
    job = db.scalar(select(Job).where(Job.id == job_id, Job.recruiter_id == recruiter_id))
    if job is None:
        raise JobNotFoundError(job_id)
    return job


def get_job_detail(db: Session, recruiter_id: int, job_id: int) -> RecruiterJobRowOut:
    job = _get_owned_job(db, recruiter_id, job_id)
    applications = list(db.scalars(select(JobApplication).where(JobApplication.job_id == job.id)))
    return _to_row(job, applications)


def set_job_status(db: Session, recruiter_id: int, job_id: int, status: str) -> RecruiterJobRowOut:
    job = _get_owned_job(db, recruiter_id, job_id)
    job.status = status
    db.commit()
    db.refresh(job)
    applications = list(db.scalars(select(JobApplication).where(JobApplication.job_id == job.id)))
    return _to_row(job, applications)
