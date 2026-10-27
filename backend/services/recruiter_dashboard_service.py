"""Recruiter Dashboard aggregation — phase.md Phase 11.

spec.md's Recruiter Dashboard SDD: "the displayed statistics, jobs,
applications, candidates, interviews, statuses and activities must
ultimately come from the Recruiter account's data." Upcoming Interviews
reads real `Interview` rows once Phase 15's Interview Agent schedules them
— before that, or for a recruiter with nothing scheduled, it is genuinely
empty rather than fabricated.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.jobs import Job, JobApplication
from backend.schemas.recruiter_dashboard import (
    ApplicationPipelineOut,
    JobRowOut,
    PipelineSliceOut,
    RecentActivityItemOut,
    RecentApplicationOut,
    RecruiterDashboardOut,
    RecruiterSummaryOut,
    UpcomingInterviewOut,
)
from backend.services.application_status import (
    ai_status_label,
    candidate_name,
    is_ai_shortlisted,
    is_awaiting_decision,
    is_recruiter_rejected,
)
from backend.services.time_format import relative_time

_RECENT_APPLICATIONS_LIMIT = 5
_RECENT_ACTIVITY_LIMIT = 4


def get_dashboard(db: Session, recruiter_id: int) -> RecruiterDashboardOut:
    jobs = list(db.scalars(select(Job).where(Job.recruiter_id == recruiter_id)))
    job_ids = [j.id for j in jobs]
    applications = (
        list(
            db.scalars(
                select(JobApplication)
                .where(JobApplication.job_id.in_(job_ids))
                .order_by(JobApplication.applied_at.desc())
            )
        )
        if job_ids
        else []
    )

    # Recruiter Dashboard — Final Specification §1/§3/§10: Shortlisted and
    # Under Review are deliberately *not* mutually exclusive — an
    # AI-shortlisted application awaiting a recruiter decision counts as
    # both at once. Rejected counts only a recruiter's own
    # Human-in-the-Loop disapproval, never the AI's own "rejected"
    # recommendation.
    shortlisted = sum(1 for a in applications if is_ai_shortlisted(a))
    under_review = sum(1 for a in applications if is_awaiting_decision(a))
    rejected = sum(1 for a in applications if is_recruiter_rejected(a))

    summary = RecruiterSummaryOut(
        total_jobs=len(jobs),
        total_applications=len(applications),
        shortlisted=shortlisted,
        under_review=under_review,
    )

    job_rows = []
    for job in jobs:
        job_apps = [a for a in applications if a.job_id == job.id]
        job_rows.append(
            JobRowOut(
                id=job.id,
                job_title=job.job_title,
                applications=len(job_apps),
                shortlisted=sum(1 for a in job_apps if is_ai_shortlisted(a)),
                under_review=sum(1 for a in job_apps if is_awaiting_decision(a)),
                rejected=sum(1 for a in job_apps if is_recruiter_rejected(a)),
                status="Active" if job.status == "active" else "Paused",
            )
        )

    total_apps = len(applications) or 1  # avoid div-by-zero when nothing has been applied yet
    pipeline = ApplicationPipelineOut(
        total=len(applications),
        shortlisted=PipelineSliceOut(
            count=shortlisted, percentage=round(shortlisted / total_apps * 100)
        ),
        under_review=PipelineSliceOut(
            count=under_review, percentage=round(under_review / total_apps * 100)
        ),
        rejected=PipelineSliceOut(count=rejected, percentage=round(rejected / total_apps * 100)),
    )

    recent_applications = [
        RecentApplicationOut(
            id=a.id,
            candidate_name=candidate_name(db, a.student_id),
            job_role=a.job.job_role,
            applied_relative=relative_time(a.applied_at),
            ai_status=ai_status_label(a),
        )
        for a in applications[:_RECENT_APPLICATIONS_LIMIT]
    ]

    upcoming_interviews = sorted(
        (
            UpcomingInterviewOut(
                candidate_name=candidate_name(db, a.student_id),
                job_role=a.job.job_role,
                scheduled_at=a.interview.scheduled_at,
                status=a.interview.status.title(),
            )
            for a in applications
            if a.interview and a.interview.status == "scheduled" and a.interview.scheduled_at
        ),
        key=lambda i: i.scheduled_at,
    )[:_RECENT_APPLICATIONS_LIMIT]

    activity_events: list[tuple[datetime, RecentActivityItemOut]] = []
    for job in jobs:
        activity_events.append(
            (
                job.created_at,
                RecentActivityItemOut(
                    label="Job created",
                    detail=job.job_title,
                    relative_time=relative_time(job.created_at),
                ),
            )
        )
    for application in applications:
        activity_events.append(
            (
                application.applied_at,
                RecentActivityItemOut(
                    label="New application received",
                    detail=(
                        f"{candidate_name(db, application.student_id)} applied for "
                        f"{application.job.job_role}"
                    ),
                    relative_time=relative_time(application.applied_at),
                ),
            )
        )
    activity_events.sort(key=lambda pair: pair[0], reverse=True)
    recent_activity = [item for _, item in activity_events[:_RECENT_ACTIVITY_LIMIT]]

    return RecruiterDashboardOut(
        summary=summary,
        jobs=job_rows,
        pipeline=pipeline,
        recent_applications=recent_applications,
        upcoming_interviews=upcoming_interviews,
        recent_activity=recent_activity,
    )
