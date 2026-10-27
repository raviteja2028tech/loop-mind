"""Student Intelligence endpoints — phase.md Phase 06. Exposes the
multi-agent system for the (later) Skill Gap / Preparation Plan pages
(Phase 08/09) to consume; no page is built here."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.intelligence import (
    PreparationPlanOut,
    SkillGapAnalysisOut,
    TargetContext,
    WhatIfRequest,
    WhatIfResultOut,
)
from backend.services import intelligence_service as service

router = APIRouter(prefix="/students/me", tags=["intelligence"])
require_student = require_role("student")


def _handle_not_found(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except service.CompanyNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No company intelligence found for '{exc}'"
        ) from exc


@router.post("/skill-gap-analysis", response_model=SkillGapAnalysisOut)
def create_skill_gap_analysis(
    payload: TargetContext,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> SkillGapAnalysisOut:
    record = _handle_not_found(
        service.analyze_skill_gap, db, account.id, payload.company_name, payload.target_role
    )
    return SkillGapAnalysisOut.model_validate(record, from_attributes=True)


@router.post("/preparation-plan", response_model=PreparationPlanOut)
def create_preparation_plan(
    payload: TargetContext,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> PreparationPlanOut:
    record = _handle_not_found(
        service.generate_preparation_plan, db, account.id, payload.company_name, payload.target_role
    )
    return PreparationPlanOut.model_validate(record, from_attributes=True)


@router.post("/what-if", response_model=WhatIfResultOut)
def create_what_if(
    payload: WhatIfRequest,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> WhatIfResultOut:
    record = _handle_not_found(
        service.ask_what_if,
        db,
        account.id,
        payload.company_name,
        payload.target_role,
        payload.question,
    )
    return WhatIfResultOut.model_validate(record, from_attributes=True)
