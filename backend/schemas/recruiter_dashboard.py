"""Recruiter Dashboard — phase.md Phase 11."""

from datetime import datetime

from pydantic import BaseModel


class RecruiterSummaryOut(BaseModel):
    """Recruiter Dashboard — Final Specification §1: exactly these four
    fields — no separate Pending Approval field, and Rejected is
    deliberately not part of this first-row summary (it's still tracked,
    just in `ApplicationPipelineOut` below, not duplicated here)."""

    total_jobs: int
    total_applications: int
    shortlisted: int
    under_review: int


class JobRowOut(BaseModel):
    id: int
    job_title: str
    applications: int
    shortlisted: int
    under_review: int
    rejected: int
    status: str


class PipelineSliceOut(BaseModel):
    count: int
    percentage: int


class ApplicationPipelineOut(BaseModel):
    """No separate Pending Approval slice (Recruiter Dashboard — Final
    Specification) — Rejected still appears here (the pipeline breakdown
    is not the same thing as the four-card summary row above)."""

    total: int
    shortlisted: PipelineSliceOut
    under_review: PipelineSliceOut
    rejected: PipelineSliceOut


class RecentApplicationOut(BaseModel):
    id: int
    candidate_name: str
    job_role: str
    applied_relative: str
    ai_status: str


class UpcomingInterviewOut(BaseModel):
    candidate_name: str
    job_role: str
    scheduled_at: datetime
    status: str


class RecentActivityItemOut(BaseModel):
    label: str
    detail: str | None
    relative_time: str


class RecruiterDashboardOut(BaseModel):
    summary: RecruiterSummaryOut
    jobs: list[JobRowOut]
    pipeline: ApplicationPipelineOut
    recent_applications: list[RecentApplicationOut]
    upcoming_interviews: list[UpcomingInterviewOut]
    recent_activity: list[RecentActivityItemOut]
