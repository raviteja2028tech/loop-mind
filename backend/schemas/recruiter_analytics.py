"""Recruiter Analytics & Historical Intelligence — phase.md Phase 17.

spec.md §3.2 names seven areas this page must support: recruitment
analytics, candidate outcomes, skill trends, recruitment-stage trends,
historical company patterns, successful-candidate characteristics, and
student skill-gap trends. No reference layout/screenshot exists for this
page (unlike Dashboard/Jobs/Candidates/Interviews), so the shape below is
this build's own design — every field is still a genuine aggregate over
the recruiter's own stored data, never a fabricated/placeholder value.
"""

from pydantic import BaseModel


class FunnelStageOut(BaseModel):
    label: str
    count: int


class OutcomeSliceOut(BaseModel):
    label: str
    count: int


class SkillTrendOut(BaseModel):
    skill: str
    count: int


class StageTrendPointOut(BaseModel):
    period: str
    applications: int


class CompanyPatternOut(BaseModel):
    job_id: int
    job_title: str
    job_role: str
    applications: int
    hire_rate_percentage: int
    average_ai_score: int | None


class SuccessfulCandidateProfileOut(BaseModel):
    total_hired: int
    average_ai_score: int | None
    top_skills: list[str]


class RecruiterAnalyticsOut(BaseModel):
    funnel: list[FunnelStageOut]
    outcomes: list[OutcomeSliceOut]
    skill_trends: list[SkillTrendOut]
    skill_gap_trends: list[SkillTrendOut]
    stage_trends: list[StageTrendPointOut]
    company_patterns: list[CompanyPatternOut]
    successful_candidate_profile: SuccessfulCandidateProfileOut
