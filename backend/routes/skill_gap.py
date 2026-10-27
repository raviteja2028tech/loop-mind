"""Skill Gap Analysis page endpoints — phase.md Phase 08. The core
analysis compute/store endpoints (/skill-gap-analysis, /preparation-plan,
/what-if) already exist from Phase 06 (backend/routes/intelligence.py);
this module only adds what the page itself needs: the shaped page payload
and target-selection support.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.skill_gap import SkillGapPageOut, TargetIn
from backend.services import skill_gap_page_service as service
from backend.services.intelligence_service import CompanyNotFoundError

router = APIRouter(prefix="/students/me/skill-gap", tags=["skill-gap"])
require_student = require_role("student")


@router.get("", response_model=SkillGapPageOut)
def get_skill_gap_page(
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> SkillGapPageOut:
    try:
        return service.get_skill_gap_page(db, account.id)
    except CompanyNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No company intelligence found for '{exc}'"
        ) from exc


@router.put("/target", response_model=SkillGapPageOut)
def put_target(
    payload: TargetIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> SkillGapPageOut:
    try:
        return service.set_target_and_refresh(
            db, account.id, payload.company_name, payload.target_role
        )
    except CompanyNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No company intelligence found for '{exc}'"
        ) from exc


@router.get("/role-options", response_model=list[str])
def get_role_options(
    company_name: str = Query(...),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> list[str]:
    return service.list_role_options(db, company_name)
