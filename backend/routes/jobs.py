"""Student Jobs & Application System endpoints — phase.md Phase 10."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, require_role
from backend.core.database import get_db
from backend.schemas.jobs import ApplicationOut, ApplyValidationOut, JobsPageOut
from backend.services import jobs_service as service

router = APIRouter(prefix="/students/me/jobs", tags=["jobs"])
require_student = require_role("student")


@router.get("", response_model=JobsPageOut)
def get_jobs_page(
    search: str | None = Query(None),
    company: list[str] = Query(default=[]),
    job_role: list[str] = Query(default=[]),
    location: list[str] = Query(default=[]),
    job_type: list[str] = Query(default=[]),
    experience_level: list[str] = Query(default=[]),
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> JobsPageOut:
    jobs = service.list_jobs(
        db,
        account.id,
        search=search,
        companies=company,
        job_roles=job_role,
        locations=location,
        job_types=job_type,
        experience_levels=experience_level,
    )
    return JobsPageOut(
        summary=service.get_summary(db, account.id),
        filters=service.list_filter_options(db),
        jobs=jobs,
    )


@router.get("/applications", response_model=list[ApplicationOut])
def get_my_applications(
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> list[ApplicationOut]:
    return service.list_my_applications(db, account.id)


@router.post("/{job_id}/save", response_model=dict[str, bool])
def toggle_save(
    job_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> dict[str, bool]:
    try:
        saved = service.toggle_saved(db, account.id, job_id)
    except service.JobNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found") from exc
    return {"saved": saved}


@router.post("/{job_id}/apply", response_model=ApplicationOut)
def apply_to_job(
    job_id: int,
    db: Session = Depends(get_db),
    account: CurrentAccount = Depends(require_student),
) -> ApplicationOut:
    try:
        result = service.apply_to_job(db, account.id, job_id)
    except service.JobNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found") from exc
    if isinstance(result, ApplyValidationOut):
        raise HTTPException(status.HTTP_409_CONFLICT, result.model_dump())
    return result
