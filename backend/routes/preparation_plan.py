"""Preparation Plan page endpoints — phase.md Phase 09. The core
generate/store action (/preparation-plan) already exists from Phase 06
(backend/routes/intelligence.py) and stays the entry point the Skill Gap
page's "Get Personalized Plan" uses; this module adds what the page
itself needs: the shaped page payload, its own generate action, and goal
tracking.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.preparation_plan_page import (
    GenerateIn,
    GoalIn,
    GoalOut,
    PreparationPlanPageOut,
)
from backend.services import preparation_plan_page_service as service
from backend.services.intelligence_service import CompanyNotFoundError

router = APIRouter(prefix="/students/me/preparation-plan-page", tags=["preparation-plan"])
require_student = require_role("student")


@router.get("", response_model=PreparationPlanPageOut)
def get_page(
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> PreparationPlanPageOut:
    return service.get_page(db, account.id)


@router.post("/generate", response_model=PreparationPlanPageOut)
def generate(
    payload: GenerateIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> PreparationPlanPageOut:
    try:
        return service.generate_plan(
            db, account.id, payload.company_name, payload.target_role, payload.academic_year
        )
    except CompanyNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No company intelligence found for '{exc}'"
        ) from exc


@router.get("/goals", response_model=dict[str, list[GoalOut]])
def get_goals(
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> dict[str, list[GoalOut]]:
    short_term, long_term = service.list_goals(db, account.id)
    return {"short_term_goals": short_term, "long_term_goals": long_term}


@router.post("/goals", response_model=dict[str, list[GoalOut]])
def add_goal(
    payload: GoalIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> dict[str, list[GoalOut]]:
    short_term, long_term = service.add_goal(db, account.id, payload.kind, payload.text)
    return {"short_term_goals": short_term, "long_term_goals": long_term}


@router.put("/goals/{goal_id}/toggle", response_model=dict[str, list[GoalOut]])
def toggle_goal(
    goal_id: str,
    kind: str,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> dict[str, list[GoalOut]]:
    short_term, long_term = service.toggle_goal(db, account.id, kind, goal_id)
    return {"short_term_goals": short_term, "long_term_goals": long_term}
