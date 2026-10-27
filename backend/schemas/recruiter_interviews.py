"""Recruiter Interviews Page — phase.md Phase 15."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from backend.schemas.recruiter_candidates import JobOptionOut
from backend.schemas.recruiter_dashboard import RecentActivityItemOut


class InterviewSummaryOut(BaseModel):
    total_interviews: int
    scheduled: int
    completed: int
    cancelled: int


class InterviewFilterOptionsOut(BaseModel):
    jobs: list[JobOptionOut]
    statuses: list[str]


class InterviewRowOut(BaseModel):
    application_id: int
    candidate_name: str
    job_id: int
    job_role: str
    interview_type: str | None
    scheduled_at: datetime | None
    scheduled_at_display: str | None
    ai_status_label: str
    status_label: str
    outcome_label: str | None


class EligibleCandidateOut(BaseModel):
    application_id: int
    candidate_name: str
    job_role: str


class InterviewsPageOut(BaseModel):
    summary: InterviewSummaryOut
    filters: InterviewFilterOptionsOut
    interviews: list[InterviewRowOut]
    eligible_candidates: list[EligibleCandidateOut]
    recent_activity: list[RecentActivityItemOut]


class QuestionOut(BaseModel):
    question_text: str
    category: str | None
    evaluation_criteria: str | None


class InterviewDetailOut(BaseModel):
    candidate_name: str
    job_role: str
    interview_type: str | None
    scheduled_at_display: str | None
    ai_status_label: str
    status_label: str
    questions: list[QuestionOut]
    invitation_subject: str | None
    invitation_body: str | None
    missing_skills: list[str]
    outcome: str | None
    outcome_label: str | None
    outcome_reason: str | None
    # Recruiter Interview Invitation & Demo Email Specification §10-11: the
    # real, persisted delivery state — never a permanent success tick.
    email_status: str
    email_status_label: str
    recipient_email: str | None
    email_source: str | None
    email_sent_at_display: str | None
    email_error: str | None


class ScheduleIn(BaseModel):
    interview_type: str
    scheduled_at: datetime


class InterviewStatusIn(BaseModel):
    status: Literal["scheduled", "completed", "cancelled"]


class OutcomeIn(BaseModel):
    outcome: Literal["hired", "not_selected"]
    reason: str | None = None
