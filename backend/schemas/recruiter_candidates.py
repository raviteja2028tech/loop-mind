"""Recruiter Candidates Page & Recruitment AI System — phase.md Phase 13.
`DisapproveIn` is Phase 14 (Human Approval & Recruitment Outcome)."""

from pydantic import BaseModel


class CandidateSummaryOut(BaseModel):
    """Recruiter Dashboard — Final Specification: no separate Pending
    Approval field here either — this page's own Shortlisted/Under
    Review/Rejected stay based on `bucket()`'s per-candidate human-
    decision status, unchanged."""

    total_candidates: int
    shortlisted: int
    under_review: int
    rejected: int


class JobOptionOut(BaseModel):
    id: int
    job_title: str


class CandidateFilterOptionsOut(BaseModel):
    jobs: list[JobOptionOut]
    statuses: list[str]
    ai_evaluations: list[str]


class CandidateRowOut(BaseModel):
    application_id: int
    candidate_name: str
    job_id: int
    job_title: str
    applied_role: str
    applied_relative: str
    ai_score: int | None
    matching_factors: str | None
    status_label: str
    ai_evaluation_label: str


class CandidatesPageOut(BaseModel):
    summary: CandidateSummaryOut
    filters: CandidateFilterOptionsOut
    candidates: list[CandidateRowOut]


class WorkflowStageOut(BaseModel):
    key: str
    label: str
    state: str


class SelectedCandidateOut(BaseModel):
    candidate_name: str
    applied_role: str
    ai_score: int | None


class CandidateWorkflowOut(BaseModel):
    selected_candidate: SelectedCandidateOut
    stages: list[WorkflowStageOut]
    matching_factors: str | None
    matched_skills: list[str]
    missing_skills: list[str]
    human_decision: str | None = None
    disapproval_reason: str | None = None
    # phase.md Phase 16: a real, historical signal — computed from this
    # recruiter's own previously-hired candidates for the same job role —
    # surfaced read-only; it never adjusts `ai_score` itself.
    historical_signal: str | None = None
    # Recruiter Interview Invitation & Demo Email Specification §10: the
    # actual generated interview/email outcome, not just the workflow
    # stage's tick — so this page never shows a checkmark alone.
    interview_question_count: int = 0
    email_status: str | None = None
    email_status_label: str | None = None
    recipient_email: str | None = None
    email_source: str | None = None
    email_error: str | None = None


class DisapproveIn(BaseModel):
    reason: str
