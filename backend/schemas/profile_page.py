"""My Profile page — phase.md Phase 18.

Career & Placement / Learning & Preparation / Professional Links / Consent
were Phase 04 schema-only tables with no onboarding UI; this is their first
exposure. Recruitment History is deliberately NOT a separate hand-entered
form — spec.md §19 wants the student's actual recruitment history, and the
real `JobApplication`/`Interview`/`HumanApproval` rows created by Phases
10-16 already ARE that history, so it is derived from them rather than
duplicated into the otherwise-empty `StudentRecruitmentHistory` table.
"""

from pydantic import BaseModel


class CareerPlacementIn(BaseModel):
    career_interest: str | None = None
    target_job_role: str | None = None
    preferred_job_domain: str | None = None
    target_company: str | None = None
    target_role: str | None = None
    preferred_technology_skill_area: list[str] = []
    placement_interest: str | None = None
    internship_interest: str | None = None
    preferred_job_type: str | None = None
    preferred_work_location: str | None = None
    preferred_country: str | None = None
    preferred_state: str | None = None
    preferred_city: str | None = None
    remote_onsite_hybrid: str | None = None
    preferred_industry: str | None = None
    placement_status: str | None = None


class CareerPlacementOut(CareerPlacementIn):
    pass


class LearningPreparationIn(BaseModel):
    current_learning_areas: list[str] = []
    skills_currently_learning: list[str] = []
    learning_goals: list[str] = []
    areas_to_improve: list[str] = []
    current_preparation_status: str | None = None
    previous_interview_experience: str | None = None
    previous_assessment_experience: str | None = None
    technical_interview_experience: str | None = None
    coding_assessment_experience: str | None = None
    interview_preparation_status: str | None = None
    assessment_preparation_status: str | None = None


class LearningPreparationOut(LearningPreparationIn):
    pass


class ProfessionalLinksIn(BaseModel):
    github_url: str | None = None
    linkedin_url: str | None = None
    portfolio_website_url: str | None = None
    coding_profile_url: str | None = None
    other_professional_profile_url: str | None = None


class ProfessionalLinksOut(ProfessionalLinksIn):
    resume_file_path: str | None = None


class ConsentIn(BaseModel):
    consent_use_information: bool = False
    consent_learning_experience: bool = False
    consent_anonymized_intelligence: bool = False


class ConsentOut(ConsentIn):
    pass


class RecruitmentApplicationOut(BaseModel):
    company_name: str
    job_role: str
    applied_relative: str
    recruitment_stage_reached: str
    outcome: str | None


class RecruitmentHistoryOut(BaseModel):
    total_applications: int
    companies_applied_to: list[str]
    roles_applied_to: list[str]
    selected_count: int
    rejected_count: int
    hold_count: int
    applications: list[RecruitmentApplicationOut]


class ProfileOverviewOut(BaseModel):
    full_name: str | None
    degree: str | None
    college: str | None
    current_semester: str | None
    city: str | None
    state: str | None
    profile_photo_path: str | None
    has_resume: bool


class ProfileStatsOut(BaseModel):
    skills_added: int
    projects: int
    certifications: int
    job_applications: int


class MissingFieldOut(BaseModel):
    section: str
    field: str


class ProfilePageOut(BaseModel):
    overview: ProfileOverviewOut
    completion_percentage: int
    missing_fields: list[MissingFieldOut]
    stats: ProfileStatsOut


class DeleteAccountOut(BaseModel):
    deleted: bool
