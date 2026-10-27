"""Student Dashboard endpoints — phase.md Phase 07."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.dashboard import (
    CompanyOption,
    DashboardOut,
    PlacementReadinessDetailOut,
    TargetCompanyIn,
    TargetCompanyOut,
)
from backend.services import dashboard_service as service
from backend.services import intelligence_service

router = APIRouter(prefix="/students/me", tags=["dashboard"])
require_student = require_role("student")


@router.get("/dashboard", response_model=DashboardOut)
def get_dashboard(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> DashboardOut:
    return service.get_dashboard(db, account.id)


@router.get("/placement-readiness-detail", response_model=PlacementReadinessDetailOut)
def get_placement_readiness_detail(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> PlacementReadinessDetailOut:
    result = intelligence_service.get_placement_readiness_detail(db, account.id)
    return PlacementReadinessDetailOut(**result)


@router.get("/target-company", response_model=TargetCompanyOut)
def get_target_company(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> TargetCompanyOut:
    return TargetCompanyOut(company_name=service.get_target_company(db, account.id))


@router.put("/target-company", response_model=TargetCompanyOut)
def put_target_company(
    payload: TargetCompanyIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> TargetCompanyOut:
    name = service.set_target_company(db, account.id, payload.company_name)
    return TargetCompanyOut(company_name=name)


@router.get("/company-options", response_model=list[CompanyOption])
def get_company_options(
    db: Session = Depends(get_db), account: CurrentAccount = Depends(require_student)
) -> list[CompanyOption]:
    return [CompanyOption(name=name) for name in service.list_company_options(db)]
