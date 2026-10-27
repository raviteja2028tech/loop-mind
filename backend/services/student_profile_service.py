"""Business logic for the Phase 05 Student Profile onboarding endpoints.
Thin CRUD scoped to the authenticated student — no cross-student access
is possible since every query filters by `student_id`.
"""

import io

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.preparation import (
    PreparationPlan,
    SkillGapAnalysis,
    StudentProgress,
    WhatIfResult,
)
from backend.models.student_profile import (
    SkillEvidence,
    StudentAcademicInfo,
    StudentCareerPlacement,
    StudentCertification,
    StudentCodingExperience,
    StudentConsent,
    StudentLearningPreparation,
    StudentProfessionalLinks,
    StudentProfile,
    StudentProject,
    StudentSkill,
)
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
    LinkedInExtractionIn,
    OnboardingStatus,
    SkillEvidenceIn,
    StudentCertificationIn,
    StudentProjectIn,
    StudentSkillIn,
)


def _log_progress(db: Session, student_id: int, event_type: str, event_data: dict) -> None:
    """Feeds the Student Dashboard's Recent Activity (phase.md Phase 07) —
    spec.md: "Activities must be generated from actual events," never
    fabricated. Only called for real create actions, not routine edits."""
    db.add(StudentProgress(student_id=student_id, event_type=event_type, event_data=event_data))


# My Profile UPDATE SDD §6: College/University and Branch are controlled
# by the original verified academic record and never overwritten by a
# later My Profile edit — the field stays visible, just read-only. (Full
# Name is protected the same way, but only at the UI layer — see
# MyProfilePage.tsx's BasicInfoCard — since this same endpoint is also how
# a student's real name is legitimately recorded post-account-creation in
# several existing flows; only Academic Info's fields are locked here.)
_PROTECTED_ACADEMIC_INFO_FIELDS = {"college", "branch", "degree"}


def upsert_basic_info(db: Session, student_id: int, data: BasicInfoIn) -> StudentProfile:
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    if profile is None:
        profile = StudentProfile(student_id=student_id, **data.model_dump())
        db.add(profile)
        _log_progress(db, student_id, "basic_info_completed", {})
    else:
        for key, value in data.model_dump().items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


def get_basic_info(db: Session, student_id: int) -> StudentProfile | None:
    return db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))


def set_profile_photo(db: Session, student_id: int, path: str) -> StudentProfile | None:
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    if profile is None:
        return None
    profile.profile_photo_path = path
    db.commit()
    db.refresh(profile)
    return profile


def delete_profile_photo(db: Session, student_id: int) -> StudentProfile | None:
    """Skill Gap/Profile Photo/Resume Management UPDATE SDD §5: removes
    the active profile-photo reference only — the rest of the profile is
    untouched, and re-uploading afterward works exactly like the first
    upload (`set_profile_photo` above)."""
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    if profile is None:
        return None
    profile.profile_photo_path = None
    db.commit()
    db.refresh(profile)
    return profile


def get_professional_links(db: Session, student_id: int) -> StudentProfessionalLinks | None:
    return db.scalar(
        select(StudentProfessionalLinks).where(StudentProfessionalLinks.student_id == student_id)
    )


def set_resume(db: Session, student_id: int, path: str) -> StudentProfessionalLinks:
    """spec.md Jobs page §22 "Resume Validation" — no onboarding step yet
    writes this field, so the Jobs apply flow's missing-info card is
    currently this field's only way to get populated."""
    links = get_professional_links(db, student_id)
    if links is None:
        links = StudentProfessionalLinks(student_id=student_id, resume_file_path=path)
        db.add(links)
    else:
        links.resume_file_path = path
    db.commit()
    db.refresh(links)
    return links


def delete_resume(db: Session, student_id: int) -> None:
    """Resume Lifecycle, Exact Resume Parsing, Source-Aware Counts & Agent
    Cross-Check SDD §2-3 — corrects the earlier Skill Gap/Profile Photo/
    Resume Management UPDATE SDD §8 decision: deleting the active resume
    now also removes whatever is still tagged `source == "resume"`
    (skills/projects/certifications this exact resume contributed and
    that were never independently confirmed by the student or LinkedIn —
    see `_upgrade_source`), not just the file reference. Unlike a failed
    upload, this is an explicit, deliberate student action with no
    "parsing might have failed" ambiguity, so the empty-extraction guard
    `apply_resume_extraction` uses does not apply here — reconciling
    against an empty extraction is exactly the correct, intended
    behavior. Manually entered and LinkedIn-derived data (and anything
    a resume-derived record was later upgraded to) is never touched."""
    links = get_professional_links(db, student_id)
    if links is not None:
        links.resume_file_path = None
        links.resume_extracted_email = None
        db.commit()
    reconcile_resume_derived_records(db, student_id, {})


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Reads the actual text out of an uploaded resume PDF. Lives here
    (not in "AI services") because it's a mechanical file-format concern,
    not AI logic — the agent layer stays free of any file/FastAPI
    dependency and only ever receives plain text (see
    resume_parser_agent.py's `extract_from_text`). A password-protected,
    scanned/image-only, or corrupt PDF yields no extractable text; that's
    surfaced as an empty string rather than raised, so a resume upload
    still succeeds (the file itself is still saved) even when nothing can
    be extracted from it — no manual profile data is ever discarded over
    an extraction failure."""
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError

    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except (PdfReadError, ValueError):
        return ""


def set_linkedin_url(db: Session, student_id: int, url: str | None) -> StudentProfessionalLinks:
    """UPDATE SDD §5/§12: the Basic Information "LinkedIn Profile" option
    reuses the existing `professional_links.linkedin_url` column rather
    than introducing a duplicate field — only this one column is touched,
    so it never clobbers any other Professional Links data already saved."""
    links = get_professional_links(db, student_id)
    if links is None:
        links = StudentProfessionalLinks(student_id=student_id, linkedin_url=url)
        db.add(links)
    else:
        links.linkedin_url = url
    db.commit()
    db.refresh(links)
    return links


# Source/Project/Certification Synchronization SDD §10/§16/§31: a source
# is never *downgraded* — once a record is confirmed manual or LinkedIn,
# a later resume extraction finding the same name must not leave it
# eligible for resume-replacement deletion. Rank order: the higher the
# number, the more protected from `reconcile_resume_derived_records`.
_SOURCE_RANK = {"resume": 1, "linkedin": 2, "manual": 3}


def _upgrade_source(row, new_source: str) -> None:
    if _SOURCE_RANK.get(new_source, 0) > _SOURCE_RANK.get(row.source, 0):
        row.source = new_source


def _persist_extracted_records(
    db: Session, student_id: int, extraction: dict, source: str = "manual"
) -> dict[str, int]:
    """Shared by LinkedIn and resume extraction: stores whatever the
    agent genuinely found as new skill/certification/project rows,
    skipping anything the student already has (by case-insensitive name,
    regardless of source — never a duplicate row just because the same
    skill also appears in a different source) so re-running extraction
    (e.g. re-uploading a resume) never creates duplicate records. `source`
    tags newly created rows ("resume" | "linkedin") so a later resume
    replacement can reconcile only what it itself previously contributed —
    see `reconcile_resume_derived_records` below. When the name already
    exists under a *less* protected source (e.g. it was first seen on a
    resume, and this same run is a LinkedIn extraction independently
    confirming it), the existing row's source is upgraded rather than
    left as-is, so it isn't still eligible for deletion the next time a
    resume is replaced — never downgraded the other way."""
    skills_by_name = {
        s.skill_name.strip().lower(): s
        for s in db.scalars(select(StudentSkill).where(StudentSkill.student_id == student_id))
    }
    certs_by_name = {
        c.certification_name.strip().lower(): c
        for c in db.scalars(
            select(StudentCertification).where(StudentCertification.student_id == student_id)
        )
    }
    projects_by_name = {
        p.project_name.strip().lower(): p
        for p in db.scalars(select(StudentProject).where(StudentProject.student_id == student_id))
    }

    skills_added = 0
    for skill in extraction.get("skills", []):
        key = skill["skill_name"].strip().lower()
        if key in skills_by_name:
            _upgrade_source(skills_by_name[key], source)
            continue
        row = create_skill(db, student_id, StudentSkillIn(**skill), source=source)
        skills_by_name[key] = row
        skills_added += 1

    certifications_added = 0
    for cert in extraction.get("certifications", []):
        key = cert["certification_name"].strip().lower()
        if key in certs_by_name:
            _upgrade_source(certs_by_name[key], source)
            continue
        row = create_certification(db, student_id, StudentCertificationIn(**cert), source=source)
        certs_by_name[key] = row
        certifications_added += 1

    projects_added = 0
    for project in extraction.get("projects", []):
        key = project["project_name"].strip().lower()
        if key in projects_by_name:
            _upgrade_source(projects_by_name[key], source)
            continue
        row = create_project(db, student_id, StudentProjectIn(**project), source=source)
        projects_by_name[key] = row
        projects_added += 1

    db.commit()
    return {
        "skills_added": skills_added,
        "certifications_added": certifications_added,
        "projects_added": projects_added,
    }


def reconcile_resume_derived_records(
    db: Session, student_id: int, extraction: dict
) -> dict[str, int]:
    """Dynamic Resume Replacement & Student Data Synchronization SDD
    §1-5: after a resume is (re-)processed, removes skill/certification/
    project rows tagged `source == "resume"` that are no longer present
    in the freshly extracted resume — so a skill/project/certification
    dropped from a replaced resume actually stops being "current"
    resume-derived data, instead of accumulating forever. Only ever
    touches rows this exact mechanism created; a skill the student
    entered manually or edited by hand (`source == "manual"`), or one
    that came from LinkedIn (`source == "linkedin"`), is never removed by
    a resume replacement, regardless of whether it also happens to be
    absent from the new resume's text."""
    new_skill_names = {s["skill_name"].strip().lower() for s in extraction.get("skills", [])}
    new_cert_names = {
        c["certification_name"].strip().lower() for c in extraction.get("certifications", [])
    }
    new_project_names = {p["project_name"].strip().lower() for p in extraction.get("projects", [])}

    skills_removed = 0
    for skill in db.scalars(
        select(StudentSkill).where(
            StudentSkill.student_id == student_id, StudentSkill.source == "resume"
        )
    ):
        if skill.skill_name.strip().lower() not in new_skill_names:
            db.delete(skill)
            skills_removed += 1

    certifications_removed = 0
    for cert in db.scalars(
        select(StudentCertification).where(
            StudentCertification.student_id == student_id, StudentCertification.source == "resume"
        )
    ):
        if cert.certification_name.strip().lower() not in new_cert_names:
            db.delete(cert)
            certifications_removed += 1

    projects_removed = 0
    for project in db.scalars(
        select(StudentProject).where(
            StudentProject.student_id == student_id, StudentProject.source == "resume"
        )
    ):
        if project.project_name.strip().lower() not in new_project_names:
            db.delete(project)
            projects_removed += 1

    db.commit()
    return {
        "skills_removed": skills_removed,
        "certifications_removed": certifications_removed,
        "projects_removed": projects_removed,
    }


def apply_linkedin_extraction(
    db: Session, student_id: int, payload: LinkedInExtractionIn
) -> dict[str, int]:
    """UPDATE SDD §6-9: runs the LinkedIn Extraction Agent over the
    student's pasted profile text and stores only what it genuinely
    found — never a fabricated placeholder — as new skill/certification/
    project rows (skipping any the student already has). Academic info is
    deliberately not written here; see linkedin_extraction_agent.py's
    module docstring for why."""
    from backend.core.ai_bridge import ensure_ai_services_importable

    ensure_ai_services_importable()
    from agents.linkedin_extraction_agent import LinkedInExtractionAgent  # noqa: PLC0415

    set_linkedin_url(db, student_id, payload.linkedin_url)

    extraction = LinkedInExtractionAgent().run(payload.profile_text)
    return _persist_extracted_records(db, student_id, extraction, source="linkedin")


def apply_resume_extraction(db: Session, student_id: int, resume_text: str) -> dict[str, int]:
    """Student Dashboard UPDATE SDD §5/§9 + Dynamic Resume Replacement &
    Student Data Synchronization SDD §1-6: runs the Resume Parser Agent's
    real text-extraction capability over an uploaded resume PDF's actual
    content, stores whatever it genuinely found — skills, certifications,
    projects, tagged `source="resume"` — skipping anything the student
    already has, and then reconciles previously resume-derived rows
    against this same extraction so a replaced resume's removed skills/
    projects/certifications actually stop being "current" (manual/
    LinkedIn-sourced data is never touched by this). Academic/experience
    info is deliberately not written to StudentAcademicInfo/
    StudentCodingExperience here for the same no-fabrication reason as
    LinkedIn extraction: a resume's education/experience text never
    reliably supplies those tables' required LOOP-MIND-specific fields
    (current_semester, cgpa_scale, admission_year, ...) — see
    resume_parser_agent.py's module docstring."""
    from backend.core.ai_bridge import ensure_ai_services_importable

    ensure_ai_services_importable()
    from agents.resume_parser_agent import ResumeParserAgent  # noqa: PLC0415

    extraction = ResumeParserAgent().extract_from_text(resume_text)
    added = _persist_extracted_records(db, student_id, extraction, source="resume")

    # Email Invitation & Session Persistence Fix Specification §2: whatever
    # email address the resume itself literally contains, stored alongside
    # the resume file reference so the Email Agent can fall back to it when
    # `StudentProfile.email` is unavailable. Only ever *set* to a genuinely
    # found address — never cleared just because a re-uploaded resume
    # doesn't happen to state one this time (the same "must not replace an
    # existing valid email unnecessarily" rule this spec states explicitly,
    # and the same "Failed Extraction Rule" precedent immediately below for
    # skills/certifications/projects). Deliberately removing the resume
    # itself (`delete_resume`) still clears it, as that's an explicit
    # student action, not an incomplete extraction.
    new_email = extraction.get("email")
    if new_email:
        links = get_professional_links(db, student_id)
        if links is not None:
            links.resume_extracted_email = new_email
            db.commit()

    # Dynamic Resume Replacement, Skill/Project/Certification
    # Synchronization & Source-Aware Deduplication SDD §26-27 "Failed
    # Extraction Rule": a new resume that yields literally nothing across
    # every category almost certainly means parsing failed to recognize
    # this resume's format (a genuinely empty resume is not a realistic
    # upload) — never treat that as "the new resume legitimately has zero
    # skills" and wipe out valid prior resume-derived data over it. Only
    # reconcile when the new extraction found at least one item, which is
    # the legitimate "this resume genuinely doesn't list X anymore" case.
    if extraction.get("skills") or extraction.get("certifications") or extraction.get("projects"):
        reconcile_resume_derived_records(db, student_id, extraction)
    return added


def upsert_academic_info(db: Session, student_id: int, data: AcademicInfoIn) -> StudentAcademicInfo:
    info = db.scalar(
        select(StudentAcademicInfo).where(StudentAcademicInfo.student_id == student_id)
    )
    if info is None:
        info = StudentAcademicInfo(student_id=student_id, **data.model_dump())
        db.add(info)
        _log_progress(db, student_id, "academic_info_completed", {})
    else:
        for key, value in data.model_dump().items():
            if key in _PROTECTED_ACADEMIC_INFO_FIELDS:
                continue
            setattr(info, key, value)
    db.commit()
    db.refresh(info)
    return info


def get_academic_info(db: Session, student_id: int) -> StudentAcademicInfo | None:
    return db.scalar(
        select(StudentAcademicInfo).where(StudentAcademicInfo.student_id == student_id)
    )


def list_skills(db: Session, student_id: int) -> list[StudentSkill]:
    return list(db.scalars(select(StudentSkill).where(StudentSkill.student_id == student_id)))


def _find_skill_by_name(db: Session, student_id: int, name: str) -> StudentSkill | None:
    for skill in db.scalars(select(StudentSkill).where(StudentSkill.student_id == student_id)):
        if skill.skill_name.strip().lower() == name.strip().lower():
            return skill
    return None


def create_skill(
    db: Session, student_id: int, data: StudentSkillIn, source: str = "manual"
) -> StudentSkill:
    """Source-Aware Deduplication SDD §11-13/§31: the same logical skill
    must never exist as two separate rows just because it was reported by
    more than one source (or the student re-enters a name that already
    exists, e.g. one already extracted from a resume/LinkedIn) — this is
    the one place every caller (manual "Add Skill", resume extraction,
    LinkedIn extraction) goes through, so the invariant holds regardless
    of call site. An existing match is updated in place (never a
    duplicate row) and its `source` only ever upgraded, never
    downgraded — see `_upgrade_source`."""
    existing = _find_skill_by_name(db, student_id, data.skill_name)
    if existing is not None:
        for key, value in data.model_dump().items():
            setattr(existing, key, value)
        _upgrade_source(existing, source)
        db.commit()
        db.refresh(existing)
        return existing

    skill = StudentSkill(student_id=student_id, source=source, **data.model_dump())
    db.add(skill)
    _log_progress(db, student_id, "skill_added", {"skill_name": data.skill_name})
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(
    db: Session, student_id: int, skill_id: int, data: StudentSkillIn
) -> StudentSkill | None:
    """spec.md My Profile §13.2 "Edit Skill" — existing skill records can
    be edited (distinct from Projects/Certifications, which the spec only
    ever describes as add/delete, never edit)."""
    skill = db.scalar(
        select(StudentSkill).where(
            StudentSkill.id == skill_id, StudentSkill.student_id == student_id
        )
    )
    if skill is None:
        return None
    for key, value in data.model_dump().items():
        setattr(skill, key, value)
    # Dynamic Resume Replacement SDD §3-6: once the student has edited a
    # skill by hand, it's theirs — a later resume replacement must never
    # delete it just because it also happened to originate from a resume.
    skill.source = "manual"
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, student_id: int, skill_id: int) -> bool:
    skill = db.scalar(
        select(StudentSkill).where(
            StudentSkill.id == skill_id, StudentSkill.student_id == student_id
        )
    )
    if skill is None:
        return False
    db.delete(skill)
    db.commit()
    return True


def add_skill_evidence(
    db: Session, student_id: int, skill_id: int, data: SkillEvidenceIn
) -> SkillEvidence | None:
    skill = db.scalar(
        select(StudentSkill).where(
            StudentSkill.id == skill_id, StudentSkill.student_id == student_id
        )
    )
    if skill is None:
        return None
    evidence = SkillEvidence(skill_id=skill_id, **data.model_dump())
    db.add(evidence)
    # Dynamic Resume Replacement SDD §3-6: the student has now personally
    # contributed real evidence for this skill — a later resume
    # replacement must never delete it out from under that evidence.
    skill.source = "manual"
    db.commit()
    db.refresh(evidence)
    return evidence


def list_coding_experience(db: Session, student_id: int) -> list[StudentCodingExperience]:
    return list(
        db.scalars(
            select(StudentCodingExperience).where(StudentCodingExperience.student_id == student_id)
        )
    )


def create_coding_experience(
    db: Session, student_id: int, data: CodingExperienceIn
) -> StudentCodingExperience:
    entry = StudentCodingExperience(student_id=student_id, **data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def delete_coding_experience(db: Session, student_id: int, entry_id: int) -> bool:
    entry = db.scalar(
        select(StudentCodingExperience).where(
            StudentCodingExperience.id == entry_id,
            StudentCodingExperience.student_id == student_id,
        )
    )
    if entry is None:
        return False
    db.delete(entry)
    db.commit()
    return True


def list_projects(db: Session, student_id: int) -> list[StudentProject]:
    return list(db.scalars(select(StudentProject).where(StudentProject.student_id == student_id)))


def _find_project_by_name(db: Session, student_id: int, name: str) -> StudentProject | None:
    for project in db.scalars(
        select(StudentProject).where(StudentProject.student_id == student_id)
    ):
        if project.project_name.strip().lower() == name.strip().lower():
            return project
    return None


def create_project(
    db: Session, student_id: int, data: StudentProjectIn, source: str = "manual"
) -> StudentProject:
    """Source-Aware Deduplication SDD §14/§31 — see `create_skill`'s
    docstring for the full rationale; the same never-a-duplicate-row,
    never-downgrade-source invariant applies to projects."""
    existing = _find_project_by_name(db, student_id, data.project_name)
    if existing is not None:
        for key, value in data.model_dump().items():
            setattr(existing, key, value)
        _upgrade_source(existing, source)
        db.commit()
        db.refresh(existing)
        return existing

    project = StudentProject(student_id=student_id, source=source, **data.model_dump())
    db.add(project)
    _log_progress(db, student_id, "project_added", {"project_name": data.project_name})
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, student_id: int, project_id: int) -> bool:
    project = db.scalar(
        select(StudentProject).where(
            StudentProject.id == project_id, StudentProject.student_id == student_id
        )
    )
    if project is None:
        return False
    db.delete(project)
    db.commit()
    return True


def list_certifications(db: Session, student_id: int) -> list[StudentCertification]:
    return list(
        db.scalars(
            select(StudentCertification).where(StudentCertification.student_id == student_id)
        )
    )


def _find_certification_by_name(
    db: Session, student_id: int, name: str
) -> StudentCertification | None:
    for cert in db.scalars(
        select(StudentCertification).where(StudentCertification.student_id == student_id)
    ):
        if cert.certification_name.strip().lower() == name.strip().lower():
            return cert
    return None


def create_certification(
    db: Session, student_id: int, data: StudentCertificationIn, source: str = "manual"
) -> StudentCertification:
    """Source-Aware Deduplication SDD §15/§31 — see `create_skill`'s
    docstring for the full rationale; the same never-a-duplicate-row,
    never-downgrade-source invariant applies to certifications."""
    existing = _find_certification_by_name(db, student_id, data.certification_name)
    if existing is not None:
        for key, value in data.model_dump().items():
            setattr(existing, key, value)
        _upgrade_source(existing, source)
        db.commit()
        db.refresh(existing)
        return existing

    cert = StudentCertification(student_id=student_id, source=source, **data.model_dump())
    db.add(cert)
    _log_progress(
        db, student_id, "certification_added", {"certification_name": data.certification_name}
    )
    db.commit()
    db.refresh(cert)
    return cert


def set_certificate_file(
    db: Session, student_id: int, cert_id: int, path: str
) -> StudentCertification | None:
    """spec.md Certifications §7: "Field: Certificate File — The field
    must be present." Scoped to the owning student like every other
    per-record update in this module."""
    cert = db.scalar(
        select(StudentCertification).where(
            StudentCertification.id == cert_id, StudentCertification.student_id == student_id
        )
    )
    if cert is None:
        return None
    cert.certificate_file_path = path
    # Dynamic Resume Replacement SDD §3-6: the student has now personally
    # attached a certificate file — a later resume replacement must never
    # delete this certification out from under it.
    cert.source = "manual"
    db.commit()
    db.refresh(cert)
    return cert


def delete_certification(db: Session, student_id: int, cert_id: int) -> bool:
    cert = db.scalar(
        select(StudentCertification).where(
            StudentCertification.id == cert_id, StudentCertification.student_id == student_id
        )
    )
    if cert is None:
        return False
    db.delete(cert)
    db.commit()
    return True


def get_onboarding_status(db: Session, student_id: int) -> OnboardingStatus:
    return OnboardingStatus(
        basic_info_complete=get_basic_info(db, student_id) is not None,
        academic_info_complete=get_academic_info(db, student_id) is not None,
        has_skills=len(list_skills(db, student_id)) > 0,
        has_coding_experience=len(list_coding_experience(db, student_id)) > 0,
        has_projects=len(list_projects(db, student_id)) > 0,
        has_certifications=len(list_certifications(db, student_id)) > 0,
    )


def get_career_placement(db: Session, student_id: int) -> StudentCareerPlacement | None:
    return db.scalar(
        select(StudentCareerPlacement).where(StudentCareerPlacement.student_id == student_id)
    )


def upsert_career_placement(
    db: Session, student_id: int, data: CareerPlacementIn
) -> StudentCareerPlacement:
    record = get_career_placement(db, student_id)
    if record is None:
        record = StudentCareerPlacement(student_id=student_id, **data.model_dump())
        db.add(record)
    else:
        for key, value in data.model_dump().items():
            setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def get_learning_preparation(db: Session, student_id: int) -> StudentLearningPreparation | None:
    return db.scalar(
        select(StudentLearningPreparation).where(
            StudentLearningPreparation.student_id == student_id
        )
    )


def upsert_learning_preparation(
    db: Session, student_id: int, data: LearningPreparationIn
) -> StudentLearningPreparation:
    """Only the fields in `LearningPreparationIn` are touched — the
    structured `short_term_goals`/`long_term_goals` lists (phase.md Phase
    09's "Your Goals", owned by the Preparation Plan page) are left alone."""
    record = get_learning_preparation(db, student_id)
    if record is None:
        record = StudentLearningPreparation(student_id=student_id, **data.model_dump())
        db.add(record)
    else:
        for key, value in data.model_dump().items():
            setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def upsert_professional_links(
    db: Session, student_id: int, data: ProfessionalLinksIn
) -> StudentProfessionalLinks:
    """Only the link fields are touched — `resume_file_path` is owned by
    the dedicated resume-upload endpoint."""
    links = get_professional_links(db, student_id)
    if links is None:
        links = StudentProfessionalLinks(student_id=student_id, **data.model_dump())
        db.add(links)
    else:
        for key, value in data.model_dump().items():
            setattr(links, key, value)
    db.commit()
    db.refresh(links)
    return links


def get_consent(db: Session, student_id: int) -> StudentConsent | None:
    return db.scalar(select(StudentConsent).where(StudentConsent.student_id == student_id))


def upsert_consent(db: Session, student_id: int, data: ConsentIn) -> StudentConsent:
    record = get_consent(db, student_id)
    if record is None:
        record = StudentConsent(student_id=student_id, **data.model_dump())
        db.add(record)
    else:
        for key, value in data.model_dump().items():
            setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def delete_account(db: Session, student_id: int) -> None:
    """spec.md My Profile §24 "Delete Profile / Account" — removes every
    row this student owns, then the account itself, in one transaction."""
    from backend.models.jobs import (
        AIMatchResult,
        HumanApproval,
        Interview,
        JobApplication,
        SavedJob,
    )
    from backend.models.student import Student

    db.query(SkillEvidence).filter(
        SkillEvidence.skill_id.in_(
            select(StudentSkill.id).where(StudentSkill.student_id == student_id)
        )
    ).delete(synchronize_session=False)
    for model in (
        StudentSkill,
        StudentCodingExperience,
        StudentProject,
        StudentCertification,
        StudentCareerPlacement,
        StudentLearningPreparation,
        StudentProfessionalLinks,
        StudentConsent,
        StudentAcademicInfo,
        StudentProfile,
        SavedJob,
        PreparationPlan,
        SkillGapAnalysis,
        WhatIfResult,
        StudentProgress,
    ):
        db.query(model).filter(model.student_id == student_id).delete(synchronize_session=False)

    application_ids = list(
        db.scalars(select(JobApplication.id).where(JobApplication.student_id == student_id))
    )
    if application_ids:
        interview_ids = list(
            db.scalars(select(Interview.id).where(Interview.application_id.in_(application_ids)))
        )
        if interview_ids:
            from backend.models.jobs import InterviewQuestion

            db.query(InterviewQuestion).filter(
                InterviewQuestion.interview_id.in_(interview_ids)
            ).delete(synchronize_session=False)
        db.query(Interview).filter(Interview.application_id.in_(application_ids)).delete(
            synchronize_session=False
        )
        db.query(HumanApproval).filter(HumanApproval.application_id.in_(application_ids)).delete(
            synchronize_session=False
        )
        db.query(AIMatchResult).filter(AIMatchResult.application_id.in_(application_ids)).delete(
            synchronize_session=False
        )
        db.query(JobApplication).filter(JobApplication.id.in_(application_ids)).delete(
            synchronize_session=False
        )

    student = db.get(Student, student_id)
    if student is not None:
        db.delete(student)
    db.commit()
