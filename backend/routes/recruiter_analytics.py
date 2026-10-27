"""Recruiter Analytics & Historical Intelligence endpoint — phase.md Phase 17."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.recruiter_analytics import RecruiterAnalyticsOut
from backend.services import recruiter_analytics_service as service

router = APIRouter(prefix="/recruiters/me/analytics", tags=["recruiter-analytics"])
require_recruiter = require_role("recruiter")


@router.get("", response_model=RecruiterAnalyticsOut)
def get_analytics(
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> RecruiterAnalyticsOut:
    return service.get_analytics(db, account.id)
