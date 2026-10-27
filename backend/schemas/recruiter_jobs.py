"""Recruiter Job Management & Create New Job — phase.md Phase 12."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class JobCreateIn(BaseModel):
    company_name: str
    job_title: str
    job_role: str
    experience_required: str
    required_skills: list[str] = []
    # spec.md Jobs page §16-17: every job card needs these from the real
    # job record — never a generic fallback — so Job Management's own
    # Create New Job must be able to set them, not just display them.
    job_type: str | None = None
    work_mode: str | None = None
    location: str | None = None
    description: str | None = None


class JobStatusIn(BaseModel):
    status: Literal["active", "paused"]


class RecruiterJobRowOut(BaseModel):
    id: int
    company_name: str
    job_title: str
    job_role: str
    experience_required: str
    location: str | None
    job_type: str | None
    work_mode: str | None
    description: str | None
    required_skills: list[str]
    applications: int
    shortlisted: int
    under_review: int
    rejected: int
    status: str
    posted_relative: str
    created_at: datetime


class RecruiterJobsSummaryOut(BaseModel):
    total_jobs: int
    active_jobs: int
    paused_jobs: int
    total_applications: int


class RecruiterJobsPageOut(BaseModel):
    summary: RecruiterJobsSummaryOut
    jobs: list[RecruiterJobRowOut]
