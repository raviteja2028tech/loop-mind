"""Skill Gap Analysis page — phase.md Phase 08. Shapes the Phase 06
multi-agent pipeline's output (backend/services/intelligence_service.py)
into the exact card/table structure spec.md's reference layout requires.
"""

from pydantic import BaseModel


class TargetIn(BaseModel):
    company_name: str
    target_role: str | None = None


class ReadinessOut(BaseModel):
    has_analysis: bool
    readiness_percentage: int | None = None
    status_message: str | None = None
    supporting_text: str | None = None


class SkillGapOverviewOut(BaseModel):
    total_required_skills: int
    skills_you_have: int
    skills_to_improve: int
    missing_evidence: int


class SkillDistributionOut(BaseModel):
    already_strong: int
    needs_improvement: int
    missing: int
    not_relevant: int


class PriorityAreaOut(BaseModel):
    rank: int
    skill: str
    impact: str


class SkillRowOut(BaseModel):
    skill: str
    category: str
    your_level: str
    required_level: str
    status: str
    priority: str | None
    resources: str | None


class SkillGapPageOut(BaseModel):
    target_company: str | None
    target_role: str | None
    company_options: list[str]
    role_options: list[str]
    readiness: ReadinessOut
    overview: SkillGapOverviewOut
    distribution: SkillDistributionOut
    priority_areas: list[PriorityAreaOut]
    skills: list[SkillRowOut]
