"""Student Create Account UPDATE SDD: registration-draft business logic.

Every onboarding section is staged as plain JSON on `RegistrationDraft`
instead of the real profile tables. Nothing here ever creates a `Student`
row — that happens exactly once, in `create_account`, and only after the
required basic information and consent are both present. Every other
section's actual database write is deferred to that same moment, reusing
the existing `student_profile_service` functions unchanged (called with
the *real* student id that exists by then) so the migration logic is
never a second, divergent copy of the real write logic.
"""

import re

import requests
from sqlalchemy.orm import Session

from backend.core.security import create_access_token
from backend.models.registration_draft import RegistrationDraft
from backend.models.student import Student
from backend.schemas.profile_page import (
    CareerPlacementIn,
    ConsentIn,
    LearningPreparationIn,
    ProfessionalLinksIn,
)
from backend.schemas.registration import CreateAccountOut, DraftSkillIn, RegistrationDraftOut
from backend.schemas.student_profile import (
    AcademicInfoIn,
    BasicInfoIn,
    CodingExperienceIn,
    SkillEvidenceIn,
    StudentCertificationIn,
    StudentProjectIn,
    StudentSkillIn,
)
from backend.services import student_profile_service as profile_service


class DraftNotFoundError(Exception):
    """The registration-draft token's draft no longer exists (already
    consumed by a completed Create Account, or never existed)."""


class BasicInfoRequiredError(Exception):
    """Student Create Account UPDATE SDD §11: Create Account requires the
    required Basic Information to be present first."""


class ConsentRequiredError(Exception):
    """Student Create Account UPDATE SDD §10: Create Account stays
    inactive until the required consent has been given."""


def _get_draft(db: Session, draft_id: int) -> RegistrationDraft:
    draft = db.get(RegistrationDraft, draft_id)
    if draft is None:
        raise DraftNotFoundError()
    return draft


def get_draft(db: Session, draft_id: int) -> RegistrationDraftOut:
    draft = _get_draft(db, draft_id)
    data = draft.data or {}
    return RegistrationDraftOut(
        mobile_number=draft.mobile_number,
        linkedin_url=draft.linkedin_url,
        profile_photo_path=draft.profile_photo_path,
        resume_file_path=draft.resume_file_path,
        basic_info=data.get("basic_info"),
        academic_info=data.get("academic_info"),
        skills=data.get("skills", []),
        coding_experience=data.get("coding_experience", []),
        projects=data.get("projects", []),
        certifications=data.get("certifications", []),
        career_placement=data.get("career_placement"),
        learning_preparation=data.get("learning_preparation"),
        professional_links=data.get("professional_links"),
        consent=data.get("consent"),
    )


def _save_section(db: Session, draft_id: int, section: str, value) -> None:
    draft = _get_draft(db, draft_id)
    data = dict(draft.data or {})
    data[section] = value
    draft.data = data
    db.commit()


def save_basic_info(db: Session, draft_id: int, payload: BasicInfoIn) -> None:
    _save_section(db, draft_id, "basic_info", payload.model_dump(mode="json"))


def save_academic_info(db: Session, draft_id: int, payload: AcademicInfoIn) -> None:
    _save_section(db, draft_id, "academic_info", payload.model_dump(mode="json"))


def save_skills(db: Session, draft_id: int, items: list[DraftSkillIn]) -> None:
    _save_section(db, draft_id, "skills", [i.model_dump(mode="json") for i in items])


def save_coding_experience(db: Session, draft_id: int, items: list[CodingExperienceIn]) -> None:
    _save_section(db, draft_id, "coding_experience", [i.model_dump(mode="json") for i in items])


def save_projects(db: Session, draft_id: int, items: list[StudentProjectIn]) -> None:
    _save_section(db, draft_id, "projects", [i.model_dump(mode="json") for i in items])


def save_certifications(db: Session, draft_id: int, items: list[StudentCertificationIn]) -> None:
    _save_section(db, draft_id, "certifications", [i.model_dump(mode="json") for i in items])


def save_career_placement(db: Session, draft_id: int, payload: CareerPlacementIn) -> None:
    _save_section(db, draft_id, "career_placement", payload.model_dump(mode="json"))


def save_learning_preparation(db: Session, draft_id: int, payload: LearningPreparationIn) -> None:
    _save_section(db, draft_id, "learning_preparation", payload.model_dump(mode="json"))


def save_professional_links(db: Session, draft_id: int, payload: ProfessionalLinksIn) -> None:
    _save_section(db, draft_id, "professional_links", payload.model_dump(mode="json"))


def save_consent(db: Session, draft_id: int, payload: ConsentIn) -> None:
    _save_section(db, draft_id, "consent", payload.model_dump(mode="json"))


def set_linkedin_url(db: Session, draft_id: int, url: str) -> None:
    draft = _get_draft(db, draft_id)
    draft.linkedin_url = url
    db.commit()


def set_profile_photo_path(db: Session, draft_id: int, path: str) -> None:
    draft = _get_draft(db, draft_id)
    draft.profile_photo_path = path
    db.commit()


def set_resume_path(db: Session, draft_id: int, path: str) -> None:
    draft = _get_draft(db, draft_id)
    draft.resume_file_path = path
    db.commit()


def fetch_linkedin_public_text(url: str) -> str:
    """Student Create Account UPDATE SDD §5-6: the student provides only
    a LinkedIn profile URL — best-effort fetch of whatever public text is
    actually served at it. LinkedIn requires authentication for real
    profile data, so an unauthenticated fetch typically returns little or
    nothing; this never fabricates missing content, and the LinkedIn
    Extraction Agent's own no-fabrication contract still applies to
    whatever text this does return (see linkedin_extraction_agent.py's
    module docstring)."""
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException:
        return ""
    text = re.sub(r"<[^>]+>", " ", response.text)
    return re.sub(r"\s+", " ", text).strip()


def _merge_extracted_into_draft(db: Session, draft_id: int, extraction: dict) -> dict[str, int]:
    """Shared by LinkedIn URL retrieval and resume upload during
    registration: merges whatever the agent genuinely found into the
    draft's skills/certifications/projects, skipping anything already
    present by name — the same dedup contract as the post-account-
    creation versions in student_profile_service.py."""
    draft = _get_draft(db, draft_id)
    data = dict(draft.data or {})

    skills = list(data.get("skills", []))
    existing_skills = {s["skill_name"].strip().lower() for s in skills}
    skills_added = 0
    for skill in extraction.get("skills", []):
        if skill["skill_name"].strip().lower() in existing_skills:
            continue
        skills.append(DraftSkillIn(**skill, evidence=[]).model_dump(mode="json"))
        existing_skills.add(skill["skill_name"].strip().lower())
        skills_added += 1
    data["skills"] = skills

    certifications = list(data.get("certifications", []))
    existing_certs = {c["certification_name"].strip().lower() for c in certifications}
    certifications_added = 0
    for cert in extraction.get("certifications", []):
        if cert["certification_name"].strip().lower() in existing_certs:
            continue
        certifications.append(StudentCertificationIn(**cert).model_dump(mode="json"))
        existing_certs.add(cert["certification_name"].strip().lower())
        certifications_added += 1
    data["certifications"] = certifications

    projects = list(data.get("projects", []))
    existing_projects = {p["project_name"].strip().lower() for p in projects}
    projects_added = 0
    for project in extraction.get("projects", []):
        if project["project_name"].strip().lower() in existing_projects:
            continue
        projects.append(StudentProjectIn(**project).model_dump(mode="json"))
        existing_projects.add(project["project_name"].strip().lower())
        projects_added += 1
    data["projects"] = projects

    draft.data = data
    db.commit()
    return {
        "skills_added": skills_added,
        "certifications_added": certifications_added,
        "projects_added": projects_added,
    }


def apply_linkedin_extraction(db: Session, draft_id: int) -> dict[str, int]:
    from backend.core.ai_bridge import ensure_ai_services_importable

    ensure_ai_services_importable()
    from agents.linkedin_extraction_agent import LinkedInExtractionAgent  # noqa: PLC0415

    draft = _get_draft(db, draft_id)
    profile_text = fetch_linkedin_public_text(draft.linkedin_url) if draft.linkedin_url else ""
    extraction = LinkedInExtractionAgent().run(profile_text)
    return _merge_extracted_into_draft(db, draft_id, extraction)


def apply_resume_extraction(db: Session, draft_id: int, resume_text: str) -> dict[str, int]:
    from backend.core.ai_bridge import ensure_ai_services_importable

    ensure_ai_services_importable()
    from agents.resume_parser_agent import ResumeParserAgent  # noqa: PLC0415

    extraction = ResumeParserAgent().extract_from_text(resume_text)
    return _merge_extracted_into_draft(db, draft_id, extraction)


def apply_linkedin_oauth_identity(db: Session, draft_id: int, code: str) -> dict:
    """LinkedIn Profile Extraction UPDATE SDD: real "Sign In with
    LinkedIn" (OpenID Connect) — the authorized counterpart to
    `apply_linkedin_extraction` above, which keeps running unchanged for
    skills/certifications/projects via the existing best-effort public
    fetch. This function only ever handles the identity fields LinkedIn's
    `openid profile email` scopes actually return: name, email, profile
    photo. Raises `linkedin_oauth_service.LinkedInOAuthError` on any
    failure — the caller must surface that as a genuine failure state,
    never a fabricated success. Does not touch `data["basic_info"]`
    directly (that section's own schema requires fields LinkedIn can
    never supply, like date of birth); the caller pre-fills the student's
    in-progress Basic Information form with the returned name/email so
    the existing Continue → `put_basic_info` save path is unchanged."""
    import uuid  # noqa: PLC0415

    from backend.core.config import PROFILE_PHOTOS_DIR  # noqa: PLC0415
    from backend.services import linkedin_oauth_service  # noqa: PLC0415

    userinfo = linkedin_oauth_service.exchange_code_for_userinfo(code)

    picture_url = userinfo.get("picture")
    has_photo = False
    if picture_url:
        photo_bytes = linkedin_oauth_service.download_profile_photo(picture_url)
        PROFILE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        destination = PROFILE_PHOTOS_DIR / f"draft-{draft_id}-{uuid.uuid4().hex}-linkedin.jpg"
        destination.write_bytes(photo_bytes)
        set_profile_photo_path(db, draft_id, str(destination))
        has_photo = True

    return {
        "name": userinfo.get("name"),
        "email": userinfo.get("email"),
        "email_verified": bool(userinfo.get("email_verified")),
        "has_photo": has_photo,
    }


def create_account(db: Session, draft_id: int) -> CreateAccountOut:
    """Student Create Account UPDATE SDD §1/§11/§12: the only place a
    real `Student` (and its profile data) is ever created. Runs the
    required-field/consent checks first — never creates a half-valid
    account — then migrates every staged section using the exact same
    service functions the post-account-creation onboarding/My Profile
    flow uses, so this is not a second, divergent write path."""
    draft = _get_draft(db, draft_id)
    data = draft.data or {}

    basic_info_raw = data.get("basic_info")
    if not basic_info_raw:
        raise BasicInfoRequiredError()
    basic_info = BasicInfoIn(**basic_info_raw)

    consent_raw = data.get("consent") or {}
    if not (
        consent_raw.get("consent_use_information")
        and consent_raw.get("consent_learning_experience")
        and consent_raw.get("consent_anonymized_intelligence")
    ):
        raise ConsentRequiredError()
    consent = ConsentIn(**consent_raw)

    student = Student(mobile_number=draft.mobile_number)
    db.add(student)
    db.commit()
    db.refresh(student)

    profile_service.upsert_basic_info(db, student.id, basic_info)
    if draft.profile_photo_path:
        profile_service.set_profile_photo(db, student.id, draft.profile_photo_path)

    if data.get("academic_info"):
        profile_service.upsert_academic_info(
            db, student.id, AcademicInfoIn(**data["academic_info"])
        )

    for skill in data.get("skills", []):
        evidence_list = skill.get("evidence", [])
        skill_fields = {k: v for k, v in skill.items() if k != "evidence"}
        created = profile_service.create_skill(db, student.id, StudentSkillIn(**skill_fields))
        for evidence in evidence_list:
            profile_service.add_skill_evidence(
                db, student.id, created.id, SkillEvidenceIn(**evidence)
            )

    for entry in data.get("coding_experience", []):
        profile_service.create_coding_experience(db, student.id, CodingExperienceIn(**entry))

    for project in data.get("projects", []):
        profile_service.create_project(db, student.id, StudentProjectIn(**project))

    for cert in data.get("certifications", []):
        profile_service.create_certification(db, student.id, StudentCertificationIn(**cert))

    if data.get("career_placement"):
        profile_service.upsert_career_placement(
            db, student.id, CareerPlacementIn(**data["career_placement"])
        )

    if data.get("learning_preparation"):
        profile_service.upsert_learning_preparation(
            db, student.id, LearningPreparationIn(**data["learning_preparation"])
        )

    links_raw = dict(data.get("professional_links") or {})
    if draft.linkedin_url and not links_raw.get("linkedin_url"):
        links_raw["linkedin_url"] = draft.linkedin_url
    if links_raw:
        profile_service.upsert_professional_links(db, student.id, ProfessionalLinksIn(**links_raw))
    if draft.resume_file_path:
        profile_service.set_resume(db, student.id, draft.resume_file_path)

    profile_service.upsert_consent(db, student.id, consent)

    db.delete(draft)
    db.commit()

    token = create_access_token(
        account_id=student.id, role="student", mobile_number=student.mobile_number
    )
    return CreateAccountOut(token=token, role="student", redirect="/app")
