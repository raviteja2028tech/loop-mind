"""My Profile page endpoints — phase.md Phase 18.

Basic Info / Academic Info / Skills / Coding Experience / Projects /
Certifications / Resume already have routes in `routes/students.py`
(Phase 05). This module adds the page's own aggregation endpoint plus the
sections Phase 18 exposes for the first time: Career & Placement, Learning
& Preparation, Professional Links, Recruitment History, Consent, and
account deletion.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.profile_page import (
    CareerPlacementIn,
    CareerPlacementOut,
    ConsentIn,
    ConsentOut,
    DeleteAccountOut,
    LearningPreparationIn,
    LearningPreparationOut,
    ProfessionalLinksIn,
    ProfessionalLinksOut,
    ProfilePageOut,
    RecruitmentHistoryOut,
)
from backend.services import intelligence_service, profile_page_service
from backend.services import student_profile_service as service

router = APIRouter(prefix="/students/me", tags=["students-profile"])
require_student = require_role("student")


@router.get("/profile", response_model=ProfilePageOut)
def get_profile_page(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> ProfilePageOut:
    return profile_page_service.get_profile_page(db, account.id)


@router.get("/career-placement", response_model=CareerPlacementOut | None)
def get_career_placement(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> CareerPlacementOut | None:
    record = service.get_career_placement(db, account.id)
    return CareerPlacementOut.model_validate(record, from_attributes=True) if record else None


@router.put("/career-placement", response_model=CareerPlacementOut)
def put_career_placement(
    payload: CareerPlacementIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> CareerPlacementOut:
    record = service.upsert_career_placement(db, account.id, payload)
    # Placement Readiness Percentage UPDATE SDD §5: Career & Placement's
    # Target Company/Target Role write to the same StudentCareerPlacement
    # row the Dashboard and Skill Gap page's own "set target" actions do —
    # changing it here is just as much a "target changed" trigger.
    intelligence_service.refresh_skill_gap_if_target_set(db, account.id)
    return CareerPlacementOut.model_validate(record, from_attributes=True)


@router.get("/learning-preparation", response_model=LearningPreparationOut | None)
def get_learning_preparation(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> LearningPreparationOut | None:
    record = service.get_learning_preparation(db, account.id)
    return LearningPreparationOut.model_validate(record, from_attributes=True) if record else None


@router.put("/learning-preparation", response_model=LearningPreparationOut)
def put_learning_preparation(
    payload: LearningPreparationIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> LearningPreparationOut:
    record = service.upsert_learning_preparation(db, account.id, payload)
    return LearningPreparationOut.model_validate(record, from_attributes=True)


@router.get("/professional-links", response_model=ProfessionalLinksOut | None)
def get_professional_links(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> ProfessionalLinksOut | None:
    record = service.get_professional_links(db, account.id)
    return ProfessionalLinksOut.model_validate(record, from_attributes=True) if record else None


@router.put("/professional-links", response_model=ProfessionalLinksOut)
def put_professional_links(
    payload: ProfessionalLinksIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> ProfessionalLinksOut:
    record = service.upsert_professional_links(db, account.id, payload)
    return ProfessionalLinksOut.model_validate(record, from_attributes=True)


@router.get("/consent", response_model=ConsentOut | None)
def get_consent(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> ConsentOut | None:
    record = service.get_consent(db, account.id)
    return ConsentOut.model_validate(record, from_attributes=True) if record else None


@router.put("/consent", response_model=ConsentOut)
def put_consent(
    payload: ConsentIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> ConsentOut:
    record = service.upsert_consent(db, account.id, payload)
    return ConsentOut.model_validate(record, from_attributes=True)


@router.get("/recruitment-history", response_model=RecruitmentHistoryOut)
def get_recruitment_history(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> RecruitmentHistoryOut:
    return profile_page_service.get_recruitment_history(db, account.id)


@router.delete("/account", response_model=DeleteAccountOut)
def delete_account(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> DeleteAccountOut:
    service.delete_account(db, account.id)
    return DeleteAccountOut(deleted=True)
