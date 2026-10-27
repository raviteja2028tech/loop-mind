"""Recruiter Interviews Page endpoints — phase.md Phase 15."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.recruiter_interviews import (
    InterviewDetailOut,
    InterviewsPageOut,
    InterviewStatusIn,
    OutcomeIn,
    ScheduleIn,
)
from backend.services import interview_service as service
from backend.services.application_status import ApplicationNotFoundError

router = APIRouter(prefix="/recruiters/me/interviews", tags=["recruiter-interviews"])
require_recruiter = require_role("recruiter")


@router.get("", response_model=InterviewsPageOut)
def get_interviews_page(
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> InterviewsPageOut:
    return service.get_interviews_page(db, account.id)


@router.get("/{application_id}", response_model=InterviewDetailOut)
def get_interview_detail(
    application_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> InterviewDetailOut:
    try:
        return service.get_interview_detail(db, account.id, application_id)
    except ApplicationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interview not found") from exc


@router.post("/{application_id}/schedule", response_model=InterviewDetailOut)
def schedule_interview(
    application_id: int,
    payload: ScheduleIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> InterviewDetailOut:
    try:
        return service.schedule_interview(
            db,
            account.id,
            application_id,
            interview_type=payload.interview_type,
            scheduled_at=payload.scheduled_at,
        )
    except ApplicationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found") from exc
    except service.InterviewNotEligibleError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Candidate is not eligible for scheduling yet — approve the candidate and wait for "
            "interview questions to be generated first.",
        ) from exc


@router.put("/{application_id}/status", response_model=InterviewDetailOut)
def set_interview_status(
    application_id: int,
    payload: InterviewStatusIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> InterviewDetailOut:
    try:
        return service.set_interview_status(db, account.id, application_id, payload.status)
    except ApplicationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found") from exc
    except service.InterviewNotEligibleError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "No interview exists for this candidate yet."
        ) from exc


@router.put("/{application_id}/outcome", response_model=InterviewDetailOut)
def set_interview_outcome(
    application_id: int,
    payload: OutcomeIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> InterviewDetailOut:
    try:
        return service.set_interview_outcome(
            db, account.id, application_id, outcome=payload.outcome, reason=payload.reason
        )
    except ApplicationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found") from exc
    except service.InterviewNotCompletedError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "The interview must be marked Completed before recording an outcome.",
        ) from exc
