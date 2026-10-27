"""Student Create Account UPDATE SDD: registration-draft endpoints.

Authenticated by a "registration" role token (issued only by
`POST /auth/verify-otp` with purpose "register" — see auth_service.py).
Every section here stages data on a `RegistrationDraft`, never a real
`Student`/profile row; `POST /registration/create-account` is the one
endpoint that ever creates the real account.
"""

import secrets
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.config import PROFILE_PHOTOS_DIR, RESUMES_DIR
from backend.core.database import get_db
from backend.schemas.profile_page import (
    CareerPlacementIn,
    ConsentIn,
    LearningPreparationIn,
    ProfessionalLinksIn,
)
from backend.schemas.registration import (
    CreateAccountOut,
    DraftSkillIn,
    LinkedInDraftExtractionOut,
    LinkedInOAuthCodeIn,
    LinkedInOAuthConfigOut,
    LinkedInOAuthIdentityOut,
    LinkedInUrlIn,
    RegistrationDraftOut,
)
from backend.schemas.student_profile import (
    AcademicInfoIn,
    BasicInfoIn,
    CodingExperienceIn,
    StudentCertificationIn,
    StudentProjectIn,
)
from backend.services import linkedin_oauth_service
from backend.services import registration_service as service
from backend.services import student_profile_service as profile_service

router = APIRouter(prefix="/registration", tags=["registration"])
require_draft = require_role("registration")


@router.get("/draft", response_model=RegistrationDraftOut)
def get_draft(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_draft)
) -> RegistrationDraftOut:
    try:
        return service.get_draft(db, account.id)
    except service.DraftNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Registration session not found") from exc


@router.put("/draft/basic-info")
def put_basic_info(
    payload: BasicInfoIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_basic_info(db, account.id, payload)
    return {"saved": True}


@router.post("/draft/basic-info/photo")
async def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File must be an image")
    PROFILE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    raw_extension = (
        (file.filename or "").rsplit(".", 1)[-1].lower() if "." in (file.filename or "") else ""
    )
    extension = raw_extension if raw_extension in {"jpg", "jpeg", "png", "gif", "webp"} else "jpg"
    filename = f"draft-{account.id}-{uuid.uuid4().hex}.{extension}"
    destination = PROFILE_PHOTOS_DIR / filename
    destination.write_bytes(await file.read())
    service.set_profile_photo_path(db, account.id, str(destination))
    return {"saved": True}


@router.put("/draft/academic-info")
def put_academic_info(
    payload: AcademicInfoIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_academic_info(db, account.id, payload)
    return {"saved": True}


@router.put("/draft/skills")
def put_skills(
    payload: list[DraftSkillIn],
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_skills(db, account.id, payload)
    return {"saved": True}


@router.put("/draft/coding-experience")
def put_coding_experience(
    payload: list[CodingExperienceIn],
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_coding_experience(db, account.id, payload)
    return {"saved": True}


@router.put("/draft/projects")
def put_projects(
    payload: list[StudentProjectIn],
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_projects(db, account.id, payload)
    return {"saved": True}


@router.put("/draft/certifications")
def put_certifications(
    payload: list[StudentCertificationIn],
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_certifications(db, account.id, payload)
    return {"saved": True}


@router.put("/draft/career-placement")
def put_career_placement(
    payload: CareerPlacementIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_career_placement(db, account.id, payload)
    return {"saved": True}


@router.put("/draft/learning-preparation")
def put_learning_preparation(
    payload: LearningPreparationIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_learning_preparation(db, account.id, payload)
    return {"saved": True}


@router.put("/draft/professional-links")
def put_professional_links(
    payload: ProfessionalLinksIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_professional_links(db, account.id, payload)
    return {"saved": True}


@router.post("/draft/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    if (file.content_type or "") != "application/pdf":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Resume must be a PDF file")
    RESUMES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"draft-{account.id}-{uuid.uuid4().hex}.pdf"
    destination = RESUMES_DIR / filename
    pdf_bytes = await file.read()
    destination.write_bytes(pdf_bytes)
    service.set_resume_path(db, account.id, str(destination))

    resume_text = profile_service.extract_pdf_text(pdf_bytes)
    extraction_summary = (
        service.apply_resume_extraction(db, account.id, resume_text)
        if resume_text.strip()
        else {"skills_added": 0, "certifications_added": 0, "projects_added": 0}
    )
    return {"saved": True, **extraction_summary}


@router.put("/draft/linkedin-url")
def put_linkedin_url(
    payload: LinkedInUrlIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.set_linkedin_url(db, account.id, payload.linkedin_url)
    return {"saved": True}


@router.post("/draft/linkedin-extract", response_model=LinkedInDraftExtractionOut)
def extract_linkedin(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_draft)
) -> LinkedInDraftExtractionOut:
    result = service.apply_linkedin_extraction(db, account.id)
    return LinkedInDraftExtractionOut(**result)


@router.get("/draft/linkedin/oauth-config", response_model=LinkedInOAuthConfigOut)
def get_linkedin_oauth_config(
    account: CurrentAccount = Depends(require_draft),
) -> LinkedInOAuthConfigOut:
    """LinkedIn Profile Extraction UPDATE SDD: tells the frontend honestly
    whether a real "Connect to LinkedIn" flow is available — no LinkedIn
    Developer app is configured for this project yet, so this reports
    `configured=False` (and no `authorization_url`) until real
    `LINKEDIN_CLIENT_ID`/`LINKEDIN_CLIENT_SECRET` values are set, rather
    than ever pretending the button will do something it can't."""
    if not linkedin_oauth_service.is_configured():
        return LinkedInOAuthConfigOut(configured=False)
    state = secrets.token_urlsafe(16)
    return LinkedInOAuthConfigOut(
        configured=True, authorization_url=linkedin_oauth_service.build_authorization_url(state)
    )


@router.post("/draft/linkedin/oauth-callback", response_model=LinkedInOAuthIdentityOut)
def linkedin_oauth_callback(
    payload: LinkedInOAuthCodeIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> LinkedInOAuthIdentityOut:
    """Completes the authorization-code exchange server-side (the client
    secret never reaches the frontend) and returns only the identity
    fields LinkedIn's `openid profile email` scopes actually provide —
    name, email, and (via the stored draft photo) a profile picture.
    Raises a 400 with the machine-readable failure code on any failure;
    never returns a fabricated identity."""
    try:
        return LinkedInOAuthIdentityOut(
            **service.apply_linkedin_oauth_identity(db, account.id, payload.code)
        )
    except linkedin_oauth_service.LinkedInOAuthError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, {"code": exc.code, "message": exc.message}
        ) from exc


@router.put("/draft/consent")
def put_consent(
    payload: ConsentIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_draft),
) -> dict:
    service.save_consent(db, account.id, payload)
    return {"saved": True}


@router.post("/create-account", response_model=CreateAccountOut)
def create_account(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_draft)
) -> CreateAccountOut:
    try:
        return service.create_account(db, account.id)
    except service.BasicInfoRequiredError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Complete Basic Information before creating your account."
        ) from exc
    except service.ConsentRequiredError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Required consent must be given before creating your account.",
        ) from exc
    except service.DraftNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Registration session not found") from exc
