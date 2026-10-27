"""Recruitment domain — spec.md §2.7-2.11 and the Recruiter Portal SDDs.

Schema only (phase.md Phase 04). Populated starting Phase 10 (student
applications), Phase 12 (recruiter job creation) and Phase 13-15 (AI
matching, human approval, interviews).
"""

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class Job(Base):
    """spec.md Recruiter Portal "Job Management & Create New Job" — the
    only explicitly specified fields are Job Title, Job Role and
    Experience; `required_skills`/`constraints` stay open JSON rather than
    inventing a fixed constraint schema ("Do not invent a fixed constraint
    list that was not specified")."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recruiter_id: Mapped[int] = mapped_column(
        ForeignKey("recruiters.id"), nullable=False, index=True
    )
    # Denormalized onto the posting itself (rather than requiring a
    # Recruiter->company relationship that doesn't exist yet) so the Jobs
    # page (phase.md Phase 10) has a real "Company Name" to display/filter
    # by per job card, independent of when Recruiter gains its own
    # organization field.
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    job_title: Mapped[str] = mapped_column(String(200), nullable=False)
    job_role: Mapped[str] = mapped_column(String(150), nullable=False)
    experience_required: Mapped[str] = mapped_column(String(100), nullable=False)
    job_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    work_mode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_skills: Mapped[list] = mapped_column(JSON, default=list)
    constraints: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active | paused
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    applications = relationship("JobApplication", back_populates="job")


class JobApplication(Base):
    """spec.md §2.7-2.8: a student's application to a specific job."""

    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    resume_snapshot_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="applied")
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    job = relationship("Job", back_populates="applications")
    match_result = relationship("AIMatchResult", back_populates="application", uselist=False)
    approval = relationship("HumanApproval", back_populates="application", uselist=False)
    interview = relationship("Interview", back_populates="application", uselist=False)


class SavedJob(Base):
    """spec.md Jobs page "Save / Bookmark Functionality" — persistent, not
    frontend-only state."""

    __tablename__ = "saved_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False, index=True)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class AIMatchResult(Base):
    """spec.md §2.8 Matching/Shortlisting Agent output. AI Status is
    explicitly separate from the recruiter's Human Approval decision."""

    __tablename__ = "ai_match_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("job_applications.id"), unique=True, nullable=False
    )
    ai_score: Mapped[float | None] = mapped_column(nullable=True)
    matching_factors: Mapped[dict] = mapped_column(JSON, default=dict)
    ai_status: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # shortlisted | hold | rejected
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    application = relationship("JobApplication", back_populates="match_result")


class HumanApproval(Base):
    """spec.md §2.9: the mandatory recruiter cross-check. `reason` is the
    disapproval reason surfaced back to the student (spec.md "Student Jobs:
    Application & Recruiter Decision Tracking")."""

    __tablename__ = "human_approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("job_applications.id"), unique=True, nullable=False
    )
    decision: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # approved | disapproved
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    application = relationship("JobApplication", back_populates="approval")


class Interview(Base):
    """spec.md Recruiter "Interviews" page. `ai_question_status` and
    `status` are deliberately separate columns — spec.md §17 "Do not merge
    AI Status and Interview Status. They are two separate pieces of
    information."."""

    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("job_applications.id"), unique=True, nullable=False
    )
    interview_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )  # pending | scheduled | completed | cancelled
    ai_question_status: Mapped[str] = mapped_column(
        String(20), default="not_started"
    )  # not_started | generating | generated
    # Recruitment Outcome (phase.md Phase 16) — a third, separate axis from
    # both AI Status and Interview Status: only set once `status` reaches
    # "completed". `outcome_reason` reuses the "Skill Gap: <skill>" prefix
    # convention established for disapproval (Phase 14) so the student-side
    # UI can parse it identically.
    outcome: Mapped[str | None] = mapped_column(String(20), nullable=True)  # hired | not_selected
    outcome_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Recruiter Interview Invitation & Demo Email Specification §3/§11-12: a
    # real, persisted delivery record for the invitation email — separate
    # from `ai_question_status` and `status` above, the same "never merge
    # distinct pieces of information" principle §17 already establishes.
    # `email_status` never regresses to "pending"/"sending" once an actual
    # send attempt has produced a terminal "sent"/"failed" result — a
    # second approval is a no-op here (see `interview_service.
    # send_invitation_email`'s idempotency guard), never a duplicate send.
    email_status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )  # pending | sending | sent | failed
    recipient_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    email_source: Mapped[str | None] = mapped_column(String(20), nullable=True)  # profile | resume
    email_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    email_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    # Recent Activity (phase.md Phase 15) derives "Interview scheduled" /
    # "Interview completed" / "Interview cancelled" timestamps from this —
    # distinct from `scheduled_at`, which is the *future* interview time.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )

    application = relationship("JobApplication", back_populates="interview")
    questions = relationship("InterviewQuestion", back_populates="interview")


class InterviewQuestion(Base):
    """Role-specific questions generated by the Interview Agent (Phase 15)."""

    __tablename__ = "interview_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id"), nullable=False, index=True
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # spec.md Phase 15: "The source also defines: evaluation criteria;
    # rubrics" — what the interviewer should listen for in the answer.
    evaluation_criteria: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    interview = relationship("Interview", back_populates="questions")
