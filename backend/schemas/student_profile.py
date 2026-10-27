"""Request/response schemas for the Student Profile onboarding endpoints
built in phase.md Phase 05: Basic Information, Academic Information,
Current Skills (+ Evidence), Coding Experience, Projects, Certifications.
"""

import re
from datetime import date

from pydantic import BaseModel, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class BasicInfoIn(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str  # male | female | others
    email: str
    country: str
    state: str
    city: str
    # spec.md My Profile (phase.md Phase 18) Basic Information fields not
    # captured during onboarding (Phase 05) — optional, editable later from
    # the profile page itself.
    alternate_mobile_number: str | None = None
    postal_code: str | None = None
    current_location: str | None = None
    permanent_location: str | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not _EMAIL_RE.match(v):
            raise ValueError("invalid email address")
        return v

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        if v not in ("male", "female", "others"):
            raise ValueError("gender must be male, female or others")
        return v


class BasicInfoOut(BasicInfoIn):
    profile_photo_path: str | None = None


class AcademicInfoIn(BaseModel):
    college: str
    college_location: str | None = None
    degree: str
    branch: str
    specialization: str | None = None
    academic_year: str
    current_year: str
    current_semester: str
    admission_year: str
    expected_graduation_year: str
    current_cgpa: float
    cgpa_scale: str
    academic_percentage: float | None = None
    tenth_score_percentage: float | None = None
    twelfth_score_percentage: float | None = None
    # spec.md My Profile "Academic Performance" — optional, not captured
    # during onboarding (Phase 05).
    semester_wise_sgpa: list[float] = []
    backlogs: int | None = None


class SkillEvidenceIn(BaseModel):
    description: str
    link: str | None = None


class SkillEvidenceOut(SkillEvidenceIn):
    id: int


class StudentSkillIn(BaseModel):
    skill_name: str
    skill_category: str
    proficiency: str
    learning_status: str
    experience_years: float | None = None


class StudentSkillOut(StudentSkillIn):
    id: int
    evidence: list[SkillEvidenceOut] = []


class CodingExperienceIn(BaseModel):
    coding_experience: str | None = None
    programming_languages: list[str] = []
    dsa_experience: str | None = None
    competitive_programming: str | None = None  # Beginner | Inter-mediate | Expert
    coding_platforms: list[str] = []
    github_link: str | None = None


class CodingExperienceOut(CodingExperienceIn):
    id: int


class StudentProjectIn(BaseModel):
    project_name: str
    project_description: str | None = None
    project_type: str | None = None
    project_status: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    technologies_used: list[str] = []
    programming_languages: list[str] = []
    frameworks: list[str] = []
    tools: list[str] = []
    skills_demonstrated: list[str] = []
    student_role: str | None = None
    team_or_individual: str | None = None
    github_repository: str | None = None
    live_demo: str | None = None
    project_documentation: str | None = None
    project_evidence: str | None = None


class StudentProjectOut(StudentProjectIn):
    id: int


class StudentCertificationIn(BaseModel):
    certification_name: str
    issuing_organization: str | None = None
    certification_type: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    skills_covered: list[str] = []


class StudentCertificationOut(StudentCertificationIn):
    id: int
    certificate_file_path: str | None = None


class OnboardingStatus(BaseModel):
    """Drives which step the onboarding modal chain resumes at, and
    contributes to the (future, Phase 07) profile-completion percentage."""

    basic_info_complete: bool
    academic_info_complete: bool
    has_skills: bool
    has_coding_experience: bool
    has_projects: bool
    has_certifications: bool


class ResumeOut(BaseModel):
    resume_file_path: str | None
    # Populated only right after an upload that triggered extraction
    # (Student Dashboard UPDATE SDD §5/§9); 0 on a plain GET, since no
    # extraction is re-run just to read the current file path.
    skills_added: int = 0
    certifications_added: int = 0
    projects_added: int = 0


class LinkedInExtractionIn(BaseModel):
    """UPDATE SDD §6-9: no authenticated LinkedIn API/scraping access
    exists in this environment, so `profile_text` is the student's own
    pasted copy of their LinkedIn profile content — see
    linkedin_extraction_agent.py's module docstring."""

    linkedin_url: str | None = None
    profile_text: str


class LinkedInExtractionOut(BaseModel):
    """Summary of what was actually found and stored — drives the
    onboarding UI's confirmation message and the decision to skip the
    corresponding manual profile-entry steps."""

    skills_added: int
    certifications_added: int
    projects_added: int
