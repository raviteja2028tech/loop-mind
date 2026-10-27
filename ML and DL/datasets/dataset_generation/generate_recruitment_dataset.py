"""ML/DL Training Architecture SDD §1: extracts historical recruitment
records from LOOP-MIND's own database — the source of truth — into a raw
training dataset. Never invents a recruitment outcome; a row only gets a
label once the recruitment process has actually reached a final state
(recruiter disapproval, or a completed interview outcome). Applications
still in progress are included with `final_outcome=None` for visibility
but are excluded from training by the preprocessing stage.

Reuses the existing backend's own database session/models directly
(`backend.core.database`, `backend.models.jobs`, `backend.models.student_profile`)
rather than a second, duplicated data-access layer — this script only
ever reads, never writes to the application's tables.

Run directly:
    python "ML and DL/datasets/dataset_generation/generate_recruitment_dataset.py"
"""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd  # noqa: E402
from sqlalchemy import select  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from backend.core.database import SessionLocal  # noqa: E402
from backend.models.jobs import HumanApproval, Interview, Job, JobApplication  # noqa: E402
from backend.models.student_profile import StudentSkill  # noqa: E402

RAW_DATASET_PATH = Path(__file__).resolve().parents[1] / "raw" / "recruitment_history.csv"


@dataclass
class RecruitmentRecord:
    """One row per job application — ML/DL Training Architecture SDD §1's
    "raw/" conceptual schema (student, job, company, skills, matching,
    shortlisting, recruiter decision, interview result, final outcome)."""

    application_id: int
    student_id: int
    job_id: int
    company_name: str
    job_role: str
    experience_required: str
    required_skills_count: int
    student_skills_count: int
    ai_score: float | None
    ai_status: str | None
    matched_skills_count: int
    missing_skills_count: int
    recruiter_decision: str | None
    disapproval_reason_present: bool
    interview_reached: bool
    interview_outcome: str | None
    final_outcome: str | None  # "success" | "failure" | None (still in progress)


def _final_outcome(approval: HumanApproval | None, interview: Interview | None) -> str | None:
    """Recruitment History Is the Core Dataset SDD §8: both outcome
    classes matter, and neither may be fabricated — an application only
    gets a label once it has genuinely concluded."""
    if interview is not None and interview.outcome == "hired":
        return "success"
    if interview is not None and interview.outcome == "not_selected":
        return "failure"
    if approval is not None and approval.decision == "disapproved":
        return "failure"
    return None  # still in progress — not yet a concluded outcome


def _student_skill_count(db: Session, student_id: int) -> int:
    return len(list(db.scalars(select(StudentSkill).where(StudentSkill.student_id == student_id))))


def generate_records(db: Session) -> list[RecruitmentRecord]:
    applications = list(db.scalars(select(JobApplication)))
    records: list[RecruitmentRecord] = []
    for application in applications:
        job = db.get(Job, application.job_id)
        if job is None:
            continue
        match = application.match_result
        approval = application.approval
        interview = application.interview

        matching_factors = match.matching_factors if match and match.matching_factors else {}
        matched_skills = matching_factors.get("matched_skills", [])
        missing_skills = matching_factors.get("missing_skills", [])

        records.append(
            RecruitmentRecord(
                application_id=application.id,
                student_id=application.student_id,
                job_id=job.id,
                company_name=job.company_name,
                job_role=job.job_role,
                experience_required=job.experience_required,
                required_skills_count=len(job.required_skills or []),
                student_skills_count=_student_skill_count(db, application.student_id),
                ai_score=match.ai_score if match else None,
                ai_status=match.ai_status if match else None,
                matched_skills_count=len(matched_skills),
                missing_skills_count=len(missing_skills),
                recruiter_decision=approval.decision if approval else None,
                disapproval_reason_present=bool(approval and approval.reason),
                interview_reached=interview is not None,
                interview_outcome=interview.outcome if interview else None,
                final_outcome=_final_outcome(approval, interview),
            )
        )
    return records


def generate_dataset(db: Session | None = None) -> pd.DataFrame:
    """Returns the raw historical recruitment dataset as a DataFrame — one
    row per application that has ever been created, concluded or not."""
    owns_session = db is None
    db = db or SessionLocal()
    try:
        records = generate_records(db)
    finally:
        if owns_session:
            db.close()
    return pd.DataFrame([asdict(r) for r in records])


def main() -> None:
    df = generate_dataset()
    RAW_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_DATASET_PATH, index=False)
    concluded = df["final_outcome"].notna().sum() if not df.empty else 0
    print(f"Wrote {len(df)} recruitment records ({concluded} with a concluded outcome) to")
    print(f"  {RAW_DATASET_PATH}")


if __name__ == "__main__":
    main()
