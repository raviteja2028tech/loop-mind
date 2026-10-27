"""Student Intelligence outputs — spec.md Skill Gap / What-If / Preparation
Plan / closed-loop sections. Schema only (phase.md Phase 04); populated by
the Student Intelligence multi-agent system (Phase 06) and the
Preparation Plan page (Phase 09).
"""

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class SkillGapAnalysis(Base):
    """spec.md Skill Gap Analysis page — result of comparing a student
    against a target company/role's Company Intelligence."""

    __tablename__ = "skill_gap_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    target_company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    target_role: Mapped[str | None] = mapped_column(String(150), nullable=True)
    # {existing_skills, missing_skills, weak_skills, missing_evidence,
    #  readiness_percentage, priority_areas, reasoning}
    analysis: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class WhatIfResult(Base):
    """spec.md "Try What-If Analysis" — one record per question asked."""

    __tablename__ = "what_if_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    result: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class PreparationPlan(Base):
    """spec.md Preparation Plan versioning: "Every regeneration should
    create a new plan version rather than destroying the previous plan."
    `status` marks exactly one row per (student, target) as "current"."""

    __tablename__ = "preparation_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    target_company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    target_role: Mapped[str | None] = mapped_column(String(150), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="current")  # current | historical
    plan: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class StudentProgress(Base):
    """Generic progress/event log ("Student completes DSA", "Skill
    updated", ...) that later analysis re-reads to recalculate skill gaps
    and regenerate preparation plans — spec.md "Progress-Based
    Regeneration"."""

    __tablename__ = "student_progress_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    event_data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class RecruitmentOutcome(Base):
    """spec.md closed-loop diagram: the final recorded outcome of an
    application, feeding future Company Intelligence — distinct from the
    application's live status, which changes as the workflow progresses."""

    __tablename__ = "recruitment_outcomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("job_applications.id"), unique=True, nullable=False
    )
    outcome_type: Mapped[str] = mapped_column(String(50), nullable=False)
    outcome_data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
