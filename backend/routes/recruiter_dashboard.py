"""Recruiter Dashboard endpoints — phase.md Phase 11."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.recruiter_dashboard import RecruiterDashboardOut
from backend.services import recruiter_dashboard_service as service

router = APIRouter(prefix="/recruiters/me", tags=["recruiter-dashboard"])
require_recruiter = require_role("recruiter")


@router.get("/dashboard", response_model=RecruiterDashboardOut)
def get_dashboard(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_recruiter)
) -> RecruiterDashboardOut:
    return service.get_dashboard(db, account.id)
