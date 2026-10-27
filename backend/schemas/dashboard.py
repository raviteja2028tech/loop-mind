from datetime import datetime

from pydantic import BaseModel


class TargetCompanyIn(BaseModel):
    company_name: str


class TargetCompanyOut(BaseModel):
    company_name: str | None


class CompanyOption(BaseModel):
    name: str


class PlacementReadinessSummary(BaseModel):
    has_analysis: bool
    readiness_percentage: int | None = None
    status_message: str | None = None


class RecentActivityItem(BaseModel):
    label: str
    detail: str | None
    relative_time: str


class PreparationJourneyStage(BaseModel):
    key: str
    label: str
    supporting_text: str
    complete: bool


class UpcomingTask(BaseModel):
    label: str


class RecommendationCard(BaseModel):
    title: str
    type: str


class StatsPoint(BaseModel):
    category: str
    value: int


class CurrentSkillOut(BaseModel):
    skill_name: str
    proficiency: str
    evidence_count: int


class PlacementReadinessDetailOut(BaseModel):
    """Student Dashboard UPDATE SDD §11-12: backs the "View Detailed
    Analysis" modal. Live-computed from the Placement Readiness Agent
    (and Student Skill Analysis Agent) over the student's current stored
    data every time it's requested — never a stored/stale snapshot — so
    it reflects, e.g., skills a resume upload just added."""

    has_analysis: bool
    target_company: str | None = None
    target_role: str | None = None
    readiness_percentage: int | None = None
    status_message: str | None = None
    current_skills: list[CurrentSkillOut] = []
    # Skills the student is ready with *for this company/role* — the
    # Placement Readiness Agent's own `matched_skills` (meets/exceeds the
    # required proficiency level).
    ready_skills: list[str] = []


class DashboardOut(BaseModel):
    full_name: str
    profile_completion_percentage: int
    skills_count: int
    projects_count: int
    certifications_count: int
    target_company: str | None
    has_resume: bool
    placement_readiness: PlacementReadinessSummary
    recent_activity: list[RecentActivityItem]
    preparation_journey: list[PreparationJourneyStage]
    upcoming_tasks: list[UpcomingTask]
    recommended_for_you: list[RecommendationCard]
    stats: list[StatsPoint]
    updated_at: datetime
