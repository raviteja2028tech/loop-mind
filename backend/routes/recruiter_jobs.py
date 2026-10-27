"""Recruiter Job Management & Create New Job endpoints — phase.md Phase 12."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.recruiter_jobs import (
    JobCreateIn,
    JobStatusIn,
    RecruiterJobRowOut,
    RecruiterJobsPageOut,
)
from backend.services import recruiter_jobs_service as service

router = APIRouter(prefix="/recruiters/me/jobs", tags=["recruiter-jobs"])
require_recruiter = require_role("recruiter")


@router.get("", response_model=RecruiterJobsPageOut)
def get_jobs_page(
    search: str | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> RecruiterJobsPageOut:
    return service.get_jobs_page(db, account.id, search=search, status=status_filter)


@router.post("", response_model=RecruiterJobRowOut)
def create_job(
    payload: JobCreateIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> RecruiterJobRowOut:
    return service.create_job(db, account.id, payload)


@router.get("/{job_id}", response_model=RecruiterJobRowOut)
def get_job_detail(
    job_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> RecruiterJobRowOut:
    try:
        return service.get_job_detail(db, account.id, job_id)
    except service.JobNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found") from exc


@router.put("/{job_id}/status", response_model=RecruiterJobRowOut)
def set_job_status(
    job_id: int,
    payload: JobStatusIn,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_recruiter),
) -> RecruiterJobRowOut:
    try:
        return service.set_job_status(db, account.id, job_id, payload.status)
    except service.JobNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found") from exc
