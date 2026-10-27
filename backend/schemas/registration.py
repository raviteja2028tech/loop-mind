"""Student Create Account UPDATE SDD: schemas for the registration-draft
flow. Every section mirrors the shape of its corresponding "real"
onboarding schema (backend/schemas/student_profile.py,
backend/schemas/profile_page.py) exactly, so a draft can be migrated into
the real tables field-for-field at `POST /registration/create-account` —
only the storage location differs (one JSON blob on `RegistrationDraft`,
not the real profile tables) until that moment.
"""

from pydantic import BaseModel

from backend.schemas.profile_page import (
    CareerPlacementIn,
    ConsentIn,
    LearningPreparationIn,
    ProfessionalLinksIn,
)
from backend.schemas.student_profile import (
    AcademicInfoIn,
    BasicInfoIn,
    CodingExperienceIn,
    SkillEvidenceIn,
    StudentCertificationIn,
    StudentProjectIn,
    StudentSkillIn,
)


class DraftSkillIn(StudentSkillIn):
    evidence: list[SkillEvidenceIn] = []


class LinkedInUrlIn(BaseModel):
    linkedin_url: str


class LinkedInDraftExtractionOut(BaseModel):
    skills_added: int
    certifications_added: int
    projects_added: int


class LinkedInOAuthConfigOut(BaseModel):
    """LinkedIn Profile Extraction UPDATE SDD: reports honestly whether a
    real "Sign In with LinkedIn" integration is actually configured —
    `authorization_url` is only present when it is, never a URL pointing
    at credentials that don't exist."""

    configured: bool
    authorization_url: str | None = None


class LinkedInOAuthCodeIn(BaseModel):
    code: str


class LinkedInOAuthIdentityOut(BaseModel):
    name: str | None = None
    email: str | None = None
    email_verified: bool = False
    has_photo: bool = False


class RegistrationDraftOut(BaseModel):
    mobile_number: str
    linkedin_url: str | None = None
    profile_photo_path: str | None = None
    resume_file_path: str | None = None
    basic_info: BasicInfoIn | None = None
    academic_info: AcademicInfoIn | None = None
    skills: list[DraftSkillIn] = []
    coding_experience: list[CodingExperienceIn] = []
    projects: list[StudentProjectIn] = []
    certifications: list[StudentCertificationIn] = []
    career_placement: CareerPlacementIn | None = None
    learning_preparation: LearningPreparationIn | None = None
    professional_links: ProfessionalLinksIn | None = None
    consent: ConsentIn | None = None


class CreateAccountOut(BaseModel):
    token: str
    role: str
    redirect: str
