"""Student Profile onboarding endpoints — phase.md Phase 05.

All routes are scoped to the authenticated student via `require_role`;
there is no way to read or write another student's data through this
router (spec.md Phase 21 "Data isolation").
"""

import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.config import CERTIFICATES_DIR, PROFILE_PHOTOS_DIR, RESUMES_DIR
from backend.core.database import get_db
from backend.schemas.student_profile import (
    AcademicInfoIn,
    BasicInfoIn,
    BasicInfoOut,
    CodingExperienceIn,
    CodingExperienceOut,
    LinkedInExtractionIn,
    LinkedInExtractionOut,
    OnboardingStatus,
    ResumeOut,
    SkillEvidenceIn,
    SkillEvidenceOut,
    StudentCertificationIn,
    StudentCertificationOut,
    StudentProjectIn,
    StudentProjectOut,
    StudentSkillIn,
    StudentSkillOut,
)
from backend.services import intelligence_service
from backend.services import student_profile_service as service

router = APIRouter(prefix="/students/me", tags=["students"])

require_student = require_role("student")


@router.put("/basic-info", response_model=BasicInfoOut)
def put_basic_info(
    payload: BasicInfoIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> BasicInfoOut:
    profile = service.upsert_basic_info(db, account.id, payload)
    return BasicInfoOut.model_validate(profile, from_attributes=True)


@router.get("/basic-info", response_model=BasicInfoOut | None)
def get_basic_info(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> BasicInfoOut | None:
    profile = service.get_basic_info(db, account.id)
    return BasicInfoOut.model_validate(profile, from_attributes=True) if profile else None


@router.post("/basic-info/photo", response_model=BasicInfoOut)
async def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> BasicInfoOut:
    """spec.md Basic Information §8-10: optional, single photo only. The
    Camera/Photos/Files selection UI (§8) is a frontend concern — this
    endpoint just stores whichever single image file is sent."""
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File must be an image")

    PROFILE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    # phase.md Phase 21 security audit: the upload's own filename is
    # client-controlled and must never reach the filesystem path — a
    # crafted name (e.g. "x.png/../../evil") could otherwise escape
    # PROFILE_PHOTOS_DIR when naively used as an "extension". Only a
    # fixed, known-safe image extension is ever used here.
    raw_extension = (
        (file.filename or "").rsplit(".", 1)[-1].lower() if "." in (file.filename or "") else ""
    )
    extension = raw_extension if raw_extension in {"jpg", "jpeg", "png", "gif", "webp"} else "jpg"
    filename = f"{account.id}-{uuid.uuid4().hex}.{extension}"
    destination = PROFILE_PHOTOS_DIR / filename
    destination.write_bytes(await file.read())

    profile = service.set_profile_photo(db, account.id, str(destination))
    if profile is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Complete Basic Information before uploading a photo"
        )
    return BasicInfoOut.model_validate(profile, from_attributes=True)


@router.get("/basic-info/photo/file")
def download_profile_photo(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> FileResponse:
    """My Profile UPDATE SDD §4: backs the actual `<img>` on My Profile —
    like the resume, the stored photo is a filesystem path, never directly
    browsable, so this is the one place that turns "a photo exists" into
    bytes the frontend can render."""
    profile = service.get_basic_info(db, account.id)
    if not profile or not profile.profile_photo_path:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No profile photo uploaded")
    extension = profile.profile_photo_path.rsplit(".", 1)[-1].lower()
    media_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }.get(extension, "application/octet-stream")
    return FileResponse(profile.profile_photo_path, media_type=media_type)


@router.delete("/basic-info/photo", response_model=BasicInfoOut)
def delete_profile_photo(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> BasicInfoOut:
    """My Profile UPDATE SDD §5: removes the active profile-photo
    reference; the student can upload a new one afterward exactly like
    the first time."""
    profile = service.delete_profile_photo(db, account.id)
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profile not found")
    return BasicInfoOut.model_validate(profile, from_attributes=True)


@router.put("/academic-info")
def put_academic_info(
    payload: AcademicInfoIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> AcademicInfoIn:
    info = service.upsert_academic_info(db, account.id, payload)
    return AcademicInfoIn.model_validate(info, from_attributes=True)


@router.get("/academic-info", response_model=AcademicInfoIn | None)
def get_academic_info(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> AcademicInfoIn | None:
    info = service.get_academic_info(db, account.id)
    return AcademicInfoIn.model_validate(info, from_attributes=True) if info else None


@router.get("/skills", response_model=list[StudentSkillOut])
def list_skills(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> list[StudentSkillOut]:
    return [
        StudentSkillOut.model_validate(s, from_attributes=True)
        for s in service.list_skills(db, account.id)
    ]


@router.post("/skills", response_model=StudentSkillOut)
def create_skill(
    payload: StudentSkillIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> StudentSkillOut:
    skill = service.create_skill(db, account.id, payload)
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return StudentSkillOut.model_validate(skill, from_attributes=True)


@router.put("/skills/{skill_id}", response_model=StudentSkillOut)
def update_skill(
    skill_id: int,
    payload: StudentSkillIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> StudentSkillOut:
    skill = service.update_skill(db, account.id, skill_id, payload)
    if skill is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found")
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return StudentSkillOut.model_validate(skill, from_attributes=True)


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> None:
    if not service.delete_skill(db, account.id, skill_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found")
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)


@router.post("/skills/{skill_id}/evidence", response_model=SkillEvidenceOut)
def add_skill_evidence(
    skill_id: int,
    payload: SkillEvidenceIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> SkillEvidenceOut:
    evidence = service.add_skill_evidence(db, account.id, skill_id, payload)
    if evidence is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found")
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return SkillEvidenceOut.model_validate(evidence, from_attributes=True)


@router.get("/coding-experience", response_model=list[CodingExperienceOut])
def list_coding_experience(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> list[CodingExperienceOut]:
    return [
        CodingExperienceOut.model_validate(e, from_attributes=True)
        for e in service.list_coding_experience(db, account.id)
    ]


@router.post("/coding-experience", response_model=CodingExperienceOut)
def create_coding_experience(
    payload: CodingExperienceIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> CodingExperienceOut:
    entry = service.create_coding_experience(db, account.id, payload)
    return CodingExperienceOut.model_validate(entry, from_attributes=True)


@router.delete("/coding-experience/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coding_experience(
    entry_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> None:
    if not service.delete_coding_experience(db, account.id, entry_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Entry not found")


@router.get("/projects", response_model=list[StudentProjectOut])
def list_projects(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> list[StudentProjectOut]:
    return [
        StudentProjectOut.model_validate(p, from_attributes=True)
        for p in service.list_projects(db, account.id)
    ]


@router.post("/projects", response_model=StudentProjectOut)
def create_project(
    payload: StudentProjectIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> StudentProjectOut:
    project = service.create_project(db, account.id, payload)
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return StudentProjectOut.model_validate(project, from_attributes=True)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> None:
    if not service.delete_project(db, account.id, project_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)


@router.get("/certifications", response_model=list[StudentCertificationOut])
def list_certifications(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> list[StudentCertificationOut]:
    return [
        StudentCertificationOut.model_validate(c, from_attributes=True)
        for c in service.list_certifications(db, account.id)
    ]


@router.post("/certifications", response_model=StudentCertificationOut)
def create_certification(
    payload: StudentCertificationIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> StudentCertificationOut:
    cert = service.create_certification(db, account.id, payload)
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return StudentCertificationOut.model_validate(cert, from_attributes=True)


@router.post("/certifications/{cert_id}/file", response_model=StudentCertificationOut)
async def upload_certificate_file(
    cert_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> StudentCertificationOut:
    """spec.md Certifications §7: "Field: Certificate File — The field
    must be present." No format/size rules are specified, so this reuses
    the same safe-extension-allowlist pattern as the profile-photo
    upload rather than inventing new validation."""
    CERTIFICATES_DIR.mkdir(parents=True, exist_ok=True)
    raw_extension = (
        (file.filename or "").rsplit(".", 1)[-1].lower() if "." in (file.filename or "") else ""
    )
    extension = raw_extension if raw_extension in {"pdf", "jpg", "jpeg", "png"} else "pdf"
    filename = f"{account.id}-{uuid.uuid4().hex}.{extension}"
    destination = CERTIFICATES_DIR / filename
    destination.write_bytes(await file.read())

    cert = service.set_certificate_file(db, account.id, cert_id, str(destination))
    if cert is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Certification not found")
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return StudentCertificationOut.model_validate(cert, from_attributes=True)


@router.delete("/certifications/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(
    cert_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> None:
    if not service.delete_certification(db, account.id, cert_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Certification not found")
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)


@router.get("/onboarding-status", response_model=OnboardingStatus)
def onboarding_status(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> OnboardingStatus:
    return service.get_onboarding_status(db, account.id)


@router.get("/resume", response_model=ResumeOut)
def get_resume(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> ResumeOut:
    links = service.get_professional_links(db, account.id)
    return ResumeOut(resume_file_path=links.resume_file_path if links else None)


@router.get("/resume/file")
def download_resume(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> FileResponse:
    """My Profile UPDATE SDD §13: backs the Download Resume action — the
    stored resume PDF is a filesystem path, not something the frontend can
    ever request directly, so this is the one place that turns "does a
    valid resume exist" into an actual downloadable file for its owner."""
    links = service.get_professional_links(db, account.id)
    if not links or not links.resume_file_path:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No resume uploaded")
    return FileResponse(links.resume_file_path, media_type="application/pdf", filename="resume.pdf")


@router.delete("/resume", response_model=ResumeOut)
def delete_resume(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> ResumeOut:
    """Resume Lifecycle, Exact Resume Parsing, Source-Aware Counts & Agent
    Cross-Check SDD §2-3: removes the active resume reference *and*
    whatever skills/projects/certifications this resume exclusively
    contributed (`source == "resume"`, never manually confirmed or
    LinkedIn-confirmed since) — deleting a resume is a deliberate action,
    so its resume-derived contribution to the current profile genuinely
    goes away, the same way replacing it would remove what the old
    version contributed. Manually entered and LinkedIn-derived data is
    never touched. Triggers a Skill Gap recalculation immediately if a
    target is already set, since the current skill set may have changed."""
    service.delete_resume(db, account.id)
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return ResumeOut(resume_file_path=None)


@router.post("/resume", response_model=ResumeOut)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> ResumeOut:
    """spec.md Jobs page §22: the resume is explicitly required (PDF) to
    apply for a job. Student Dashboard UPDATE SDD §5/§9: every resume
    upload/replacement — from the Professional Links onboarding step or
    the Dashboard's Upload Your Resume card, same endpoint either way —
    triggers the Resume Parser Agent's real text extraction, storing any
    new skills/certifications/projects genuinely found (deduped against
    what the student already has) so they immediately feed Current
    Skills, Placement Readiness, and Skill Gap Analysis."""
    if (file.content_type or "") != "application/pdf":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Resume must be a PDF file")

    RESUMES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{account.id}-{uuid.uuid4().hex}.pdf"
    destination = RESUMES_DIR / filename
    pdf_bytes = await file.read()
    destination.write_bytes(pdf_bytes)

    links = service.set_resume(db, account.id, str(destination))

    resume_text = service.extract_pdf_text(pdf_bytes)
    extraction_summary = (
        service.apply_resume_extraction(db, account.id, resume_text)
        if resume_text.strip()
        else {"skills_added": 0, "certifications_added": 0, "projects_added": 0}
    )

    # Student Resume Upload & Skill Gap Automation SDD §2-3/§10-11: if a
    # target company is already selected (Scenario B — company chosen
    # before this resume, or this is a re-upload replacing an earlier
    # one), refresh the Skill Gap Analysis immediately so the newly
    # extracted skills are reflected without the student needing to
    # re-select their target to force a recalculation.
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)

    return ResumeOut(resume_file_path=links.resume_file_path, **extraction_summary)


@router.post("/linkedin-extract", response_model=LinkedInExtractionOut)
def extract_linkedin(
    payload: LinkedInExtractionIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> LinkedInExtractionOut:
    """UPDATE SDD §6-9: runs the LinkedIn Extraction Agent over the
    authenticated student's own pasted profile text and stores whatever
    it genuinely found, so the Create Account wizard can skip the
    corresponding manual profile-entry steps."""
    result = service.apply_linkedin_extraction(db, account.id, payload)
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return LinkedInExtractionOut(**result)
