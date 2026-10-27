"""Company Intelligence dataset — spec.md "Company Intelligence, Skill Gap
Analysis & Preparation Plan Specification" §2-4.

Distinct from `Job` (backend/models/jobs.py), which represents a real
posting created by an authenticated recruiter (Phase 12). Company
Intelligence is the historical/aggregate knowledge base — company
requirements, patterns, successful-candidate characteristics — that the
Student Intelligence multi-agent system (Phase 06) compares a student
against. Until a real dataset is supplied, it holds generated synthetic
data (backend/core/seed_company_intelligence.py), explicitly marked as
such so it is never confused with proprietary company information.
"""

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    industry: Mapped[str | None] = mapped_column(String(150), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_synthetic: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    role_requirements = relationship("CompanyRoleRequirement", back_populates="company")
    historical_requirements = relationship("CompanyHistoricalRequirement", back_populates="company")
    requirement_patterns = relationship("CompanyRequirementPattern", back_populates="company")
    successful_candidate_profiles = relationship(
        "SuccessfulCandidateProfile", back_populates="company"
    )


class CompanyRoleRequirement(Base):
    """Current job requirements for a role at a company — spec.md
    "role-specific requirements; skill requirements; experience
    expectations; evidence expectations; relevant project expectations"."""

    __tablename__ = "company_role_requirements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    role_title: Mapped[str] = mapped_column(String(150), nullable=False)
    # [{skill, min_proficiency}, ...]
    required_skills: Mapped[list] = mapped_column(JSON, default=list)
    experience_expectation: Mapped[str | None] = mapped_column(String(200), nullable=True)
    evidence_expectations: Mapped[list] = mapped_column(JSON, default=list)
    project_expectations: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    company = relationship("Company", back_populates="role_requirements")


class CompanyHistoricalRequirement(Base):
    """spec.md "historical job requirements" — snapshots of what a role
    required in a prior recruitment cycle, so requirement drift over time
    can be analyzed."""

    __tablename__ = "company_historical_requirements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    role_title: Mapped[str] = mapped_column(String(150), nullable=False)
    cycle_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    requirement_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    company = relationship("Company", back_populates="historical_requirements")


class CompanyRequirementPattern(Base):
    """spec.md "requirement patterns" — recurring recruitment patterns
    detected/declared for a company (e.g. "consistently weights DSA
    heavily for SDE roles")."""

    __tablename__ = "company_requirement_patterns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    pattern_description: Mapped[str] = mapped_column(Text, nullable=False)
    pattern_data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    company = relationship("Company", back_populates="requirement_patterns")


class SuccessfulCandidateProfile(Base):
    """spec.md dataset category 4, "Successful Candidate Dataset" —
    characteristics of candidates who were selected/placed, used by the
    Placement Readiness / Skill-Gap agents (Phase 06)."""

    __tablename__ = "successful_candidate_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    role_title: Mapped[str | None] = mapped_column(String(150), nullable=True)
    profile_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    company = relationship("Company", back_populates="successful_candidate_profiles")
