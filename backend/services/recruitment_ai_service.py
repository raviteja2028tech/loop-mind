"""Bridges JobApplication data to Multi-Agent System 2 — phase.md Phase 13.

Mirrors backend/services/intelligence_service.py's role for Multi-Agent
System 1: shape ORM rows into the plain-dict inputs the agents expect
(keeping "AI services" free of any `backend` dependency), run the
pipeline, and persist the result as a new AIMatchResult row.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.ai_bridge import ensure_ai_services_importable
from backend.models.jobs import AIMatchResult, Interview, Job, JobApplication
from backend.models.student_profile import (
    StudentAcademicInfo,
    StudentCertification,
    StudentCodingExperience,
    StudentProfessionalLinks,
    StudentProfile,
    StudentProject,
    StudentSkill,
)

ensure_ai_services_importable()

from multi_agent.recruitment_intelligence import run_recruitment_pipeline  # noqa: E402
from rag.vector_store import get_client  # noqa: E402


def _candidate_to_dict(db: Session, student_id: int) -> dict:
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    links = db.scalar(
        select(StudentProfessionalLinks).where(StudentProfessionalLinks.student_id == student_id)
    )
    skills = list(db.scalars(select(StudentSkill).where(StudentSkill.student_id == student_id)))
    projects = list(
        db.scalars(select(StudentProject).where(StudentProject.student_id == student_id))
    )
    certifications = list(
        db.scalars(
            select(StudentCertification).where(StudentCertification.student_id == student_id)
        )
    )
    coding_experience = list(
        db.scalars(
            select(StudentCodingExperience).where(StudentCodingExperience.student_id == student_id)
        )
    )
    academic = db.scalar(
        select(StudentAcademicInfo).where(StudentAcademicInfo.student_id == student_id)
    )

    return {
        "full_name": profile.full_name if profile else None,
        "email": profile.email if profile else None,
        "has_resume_on_file": bool(links and links.resume_file_path),
        "skills": [
            {
                "skill_name": s.skill_name,
                "proficiency": s.proficiency,
                "evidence_count": len(s.evidence),
            }
            for s in skills
        ],
        "projects": [{"project_name": p.project_name} for p in projects],
        "certifications": [{"certification_name": c.certification_name} for c in certifications],
        "coding_experience": [
            {"programming_languages": c.programming_languages} for c in coding_experience
        ],
        "academic": (
            {"degree": academic.degree, "branch": academic.branch, "college": academic.college}
            if academic
            else None
        ),
    }


def _job_to_dict(job: Job) -> dict:
    return {
        "job_title": job.job_title,
        "job_role": job.job_role,
        "experience_required": job.experience_required,
        "required_skills": job.required_skills,
    }


def _historical_outcome_applications(
    db: Session, application: JobApplication, outcome: str
) -> list[JobApplication]:
    recruiter_id = application.job.recruiter_id
    job_role = application.job.job_role
    return list(
        db.scalars(
            select(JobApplication)
            .join(Job, JobApplication.job_id == Job.id)
            .join(Interview, Interview.application_id == JobApplication.id)
            .where(
                Job.recruiter_id == recruiter_id,
                Job.job_role == job_role,
                Interview.outcome == outcome,
                JobApplication.id != application.id,
            )
        )
    )


def _matched_skills_of(applications: list[JobApplication]) -> set[str]:
    skills: set[str] = set()
    for application in applications:
        if application.match_result and application.match_result.matching_factors:
            skills.update(application.match_result.matching_factors.get("matched_skills", []))
    return skills


def _historical_signal(
    db: Session, application: JobApplication, matched_skills: list[str]
) -> str | None:
    """phase.md Phase 16 "Recruitment Outcome -> Future Recruitment
    Intelligence" + Recruiter Portal UPDATE SDD §17-20 "the ML system must
    not learn only from successful candidates": a real, read-only signal
    computed from this recruiter's own historical closed-loop outcomes for
    the same job role (recruiter isolation — never another recruiter's
    candidates), drawing on BOTH previously-hired and previously-rejected
    interview outcomes, not hired candidates alone. Informational only; it
    never adjusts `ai_score`."""
    if not matched_skills:
        return None

    hired = _historical_outcome_applications(db, application, "hired")
    not_selected = _historical_outcome_applications(db, application, "not_selected")
    if not hired and not not_selected:
        return None

    job_role = application.job.job_role
    matched = set(matched_skills)
    parts = []

    hired_overlap = sorted(matched & _matched_skills_of(hired))
    if hired_overlap:
        parts.append(
            f"{len(hired)} previously hired candidate(s) for {job_role} also had: "
            f"{', '.join(hired_overlap)}."
        )

    rejected_overlap = sorted(matched & _matched_skills_of(not_selected))
    if rejected_overlap:
        parts.append(
            f"{len(not_selected)} previously not-selected candidate(s) for {job_role} also had: "
            f"{', '.join(rejected_overlap)} — shared skills alone weren't the deciding factor."
        )

    return " ".join(parts) if parts else None


def ensure_match_result(db: Session, application: JobApplication) -> AIMatchResult:
    """Runs the AI recruitment pipeline for this application if it hasn't
    been evaluated yet (auto-run-on-view, matching Phase 08's Skill Gap
    page pattern) and persists the result. Idempotent — a re-view of an
    already-evaluated application returns the existing result rather than
    re-running the pipeline."""
    if application.match_result is not None:
        return application.match_result

    candidate = _candidate_to_dict(db, application.student_id)
    job = _job_to_dict(application.job)
    qdrant = get_client()
    try:
        result = run_recruitment_pipeline(
            qdrant,
            application_id=application.id,
            candidate=candidate,
            job_id=application.job_id,
            job=job,
        )
    finally:
        qdrant.close()

    matching_factors = dict(result["matching"])
    matching_factors["historical_signal"] = _historical_signal(
        db, application, matching_factors.get("matched_skills", [])
    )

    match = AIMatchResult(
        application_id=application.id,
        ai_score=result["matching"]["ai_score"],
        matching_factors=matching_factors,
        ai_status=result["shortlisting"]["ai_status"],
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match
