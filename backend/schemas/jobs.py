"""Student Jobs & Application System — phase.md Phase 10."""

from datetime import datetime

from pydantic import BaseModel


class FilterOptionsOut(BaseModel):
    companies: list[str]
    job_roles: list[str]
    locations: list[str]
    job_types: list[str]
    experience_levels: list[str]


class JobSummaryOut(BaseModel):
    total_jobs: int
    applied: int
    under_review: int
    shortlisted: int


class JobCardOut(BaseModel):
    id: int
    company_name: str
    job_title: str
    job_role: str
    location: str | None
    job_type: str | None
    work_mode: str | None
    experience_required: str
    description: str | None
    required_skills: list[str]
    status: str
    posted_relative: str
    is_saved: bool
    has_applied: bool


class JobsPageOut(BaseModel):
    summary: JobSummaryOut
    filters: FilterOptionsOut
    jobs: list[JobCardOut]


class MissingRequirementOut(BaseModel):
    field: str
    label: str
    reason: str


class ApplyValidationOut(BaseModel):
    can_apply: bool
    missing: list[MissingRequirementOut]


class ApplicationOut(BaseModel):
    id: int
    job_id: int
    job_title: str
    company_name: str
    job_role: str
    status_label: str
    disapproval_reason: str | None
    applied_at: datetime
