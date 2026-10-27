"""Recruiter Candidates Page endpoints — phase.md Phase 13.
Approve/Disapprove are Phase 14 (Human Approval & Recruitment Outcome)."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.recruiter_candidates import (
    CandidatesPageOut,
    CandidateWorkflowOut,
    DisapproveIn,
)
from backend.services import recruiter_candidates_service as service
from backend.services.application_status import ApplicationNotFoundError

router = APIRouter(prefix="/recruiters/me/candidates", tags=["recruiter-candidates"])
require_recruiter = require_role("recruiter")


@router.get("", response_model=CandidatesPageOut)
def get_candidates_page(
    search: str | None = Query(None),
    job_id: int | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    ai_evaluation: str | None = Query(None),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> CandidatesPageOut:
    return service.get_candidates_page(
        db,
        account.id,
        search=search,
        job_id=job_id,
        status=status_filter,
        ai_evaluation=ai_evaluation,
    )


@router.get("/{application_id}/workflow", response_model=CandidateWorkflowOut)
def get_workflow(
    application_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> CandidateWorkflowOut:
    try:
        return service.get_workflow(db, account.id, application_id)
    except ApplicationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found") from exc


@router.post("/{application_id}/approve", response_model=CandidateWorkflowOut)
def approve_candidate(
    application_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> CandidateWorkflowOut:
    try:
        return service.approve_candidate(db, account.id, application_id)
    except ApplicationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found") from exc


@router.post("/{application_id}/disapprove", response_model=CandidateWorkflowOut)
def disapprove_candidate(
    application_id: int,
    payload: DisapproveIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> CandidateWorkflowOut:
    try:
        return service.disapprove_candidate(db, account.id, application_id, payload.reason)
    except ApplicationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found") from exc
