"""Bridges the Student Profile / Company Intelligence database (SQLite,
the source of truth) to the Student Intelligence multi-agent system in
"AI services/" — phase.md Phase 06.

Responsibilities: shape ORM rows into the plain-dict inputs the agents
expect (keeping "AI services" free of any `backend` dependency), run the
pipeline, and persist the results as new SkillGapAnalysis / PreparationPlan
/ WhatIfResult rows.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.ai_bridge import ensure_ai_services_importable
from backend.models.company_intelligence import Company
from backend.models.preparation import PreparationPlan, SkillGapAnalysis, WhatIfResult
from backend.models.student_profile import (
    StudentAcademicInfo,
    StudentCertification,
    StudentCodingExperience,
    StudentProject,
    StudentSkill,
)

ensure_ai_services_importable()

from multi_agent.student_placement_intelligence import (  # noqa: E402
    run_student_intelligence_pipeline,
    run_what_if,
)
from rag.ingest import ingest_companies  # noqa: E402
from rag.vector_store import get_client  # noqa: E402


class CompanyNotFoundError(Exception):
    pass


def _company_to_dict(company: Company) -> dict:
    return {
        "company_id": company.id,
        "company_name": company.name,
        "industry": company.industry,
        "role_requirements": [
            {
                "role_title": r.role_title,
                "required_skills": r.required_skills,
                "experience_expectation": r.experience_expectation,
                "evidence_expectations": r.evidence_expectations,
                "project_expectations": r.project_expectations,
            }
            for r in company.role_requirements
        ],
        "patterns": [p.pattern_description for p in company.requirement_patterns],
        "historical_requirements": [
            {
                "role_title": h.role_title,
                "cycle_year": h.cycle_year,
                "requirement_snapshot": h.requirement_snapshot,
            }
            for h in company.historical_requirements
        ],
        "successful_candidate_profiles": [
            {"role_title": p.role_title, "profile_summary": p.profile_summary}
            for p in company.successful_candidate_profiles
        ],
    }


def _student_to_dict(db: Session, student_id: int) -> dict:
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
        "student_id": student_id,
        "skills": [
            {
                "skill_name": s.skill_name,
                "skill_category": s.skill_category,
                "proficiency": s.proficiency,
                "learning_status": s.learning_status,
                "experience_years": s.experience_years,
                "evidence_count": len(s.evidence),
            }
            for s in skills
        ],
        "projects": [
            {
                "project_name": p.project_name,
                "technologies_used": p.technologies_used,
                "skills_demonstrated": p.skills_demonstrated,
            }
            for p in projects
        ],
        "certifications": [
            {"certification_name": c.certification_name, "skills_covered": c.skills_covered}
            for c in certifications
        ],
        "coding_experience": [
            {
                "programming_languages": c.programming_languages,
                "competitive_programming": c.competitive_programming,
            }
            for c in coding_experience
        ],
        "academic": (
            {
                "college": academic.college,
                "degree": academic.degree,
                "branch": academic.branch,
                "current_year": academic.current_year,
                "current_cgpa": academic.current_cgpa,
            }
            if academic
            else None
        ),
    }


def ingest_company_intelligence_into_qdrant(db: Session) -> int:
    """Embeds every seeded company into Qdrant's `company_knowledge`
    collection — called once at startup (idempotent: ingest_companies
    upserts on deterministic IDs, so re-running is safe and cheap)."""
    companies = list(db.scalars(select(Company)))
    if not companies:
        return 0
    qdrant = get_client()
    try:
        return ingest_companies(qdrant, [_company_to_dict(c) for c in companies])
    finally:
        qdrant.close()


def _get_company_or_raise(db: Session, company_name: str) -> Company:
    company = db.scalar(select(Company).where(Company.name == company_name))
    if company is None:
        raise CompanyNotFoundError(company_name)
    return company


def analyze_skill_gap(
    db: Session, student_id: int, company_name: str, target_role: str | None
) -> SkillGapAnalysis:
    company = _get_company_or_raise(db, company_name)
    student = _student_to_dict(db, student_id)
    qdrant = get_client()
    try:
        result = run_student_intelligence_pipeline(
            qdrant, company=_company_to_dict(company), student=student, target_role=target_role
        )
    finally:
        qdrant.close()

    record = SkillGapAnalysis(
        student_id=student_id,
        target_company=company.name,
        target_role=result["company_intel"]["target_role"],
        analysis={
            "readiness": result["readiness"],
            "skill_gap": result["skill_gap"],
        },
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def generate_preparation_plan(
    db: Session,
    student_id: int,
    company_name: str,
    target_role: str | None,
    academic_year_override: str | None = None,
) -> PreparationPlan:
    """`academic_year_override` — phase.md Phase 09's Preparation Plan page
    lets a student preview the plan for a different academic year than
    their stored one via its own "Your Academic Year" selector; it only
    ever overrides the year fed into this pipeline, never the stored
    StudentAcademicInfo record itself."""
    company = _get_company_or_raise(db, company_name)
    student = _student_to_dict(db, student_id)
    if academic_year_override:
        academic = dict(student.get("academic") or {})
        academic["current_year"] = academic_year_override
        student = {**student, "academic": academic}
    qdrant = get_client()
    try:
        result = run_student_intelligence_pipeline(
            qdrant, company=_company_to_dict(company), student=student, target_role=target_role
        )
    finally:
        qdrant.close()

    # spec.md Preparation Plan versioning: mark any existing "current"
    # plan for this (student, company) target as historical before
    # inserting the new current version — never delete previous plans.
    previous = list(
        db.scalars(
            select(PreparationPlan).where(
                PreparationPlan.student_id == student_id,
                PreparationPlan.target_company == company.name,
            )
        )
    )
    next_version = 1
    for plan in previous:
        plan.status = "historical"
        next_version = max(next_version, plan.version + 1)

    record = PreparationPlan(
        student_id=student_id,
        target_company=company.name,
        target_role=result["company_intel"]["target_role"],
        version=next_version,
        status="current",
        plan=result["preparation_plan"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_latest_skill_gap_analysis(
    db: Session, student_id: int, target_company: str, target_role: str | None
) -> SkillGapAnalysis:
    """Placement Readiness Percentage UPDATE SDD §4 "Single Source of
    Truth": the one place that resolves "the student's current Placement
    Readiness result" for a given target — the most recent SkillGapAnalysis
    row for this exact (student, target_company), or a freshly run one if
    none exists yet. Dashboard, Skill Gap and Preparation Plan must all go
    through this (never their own independent stored-row lookup) so they
    can never diverge just because one page happened to run its own query
    differently from another."""
    latest = db.scalar(
        select(SkillGapAnalysis)
        .where(
            SkillGapAnalysis.student_id == student_id,
            SkillGapAnalysis.target_company == target_company,
        )
        .order_by(SkillGapAnalysis.created_at.desc())
    )
    if latest is None:
        latest = analyze_skill_gap(db, student_id, target_company, target_role)
    return latest


def get_readiness_summary(db: Session, student_id: int) -> dict:
    """The single Overall Placement Readiness % + status message, for
    whatever the student's current target is — the shared source Dashboard,
    Skill Gap and Preparation Plan all read (§1-4). Returns a "no analysis"
    shape, never a fabricated percentage, when no target company is set."""
    target_company, target_role = _get_target(db, student_id)
    if target_company is None:
        return {"has_analysis": False, "readiness_percentage": None, "status_message": None}
    latest = get_latest_skill_gap_analysis(db, student_id, target_company, target_role)
    readiness = latest.analysis["readiness"]
    return {
        "has_analysis": True,
        "readiness_percentage": readiness["readiness_percentage"],
        "status_message": readiness["status_message"],
    }


def refresh_skill_gap_if_target_set(db: Session, student_id: int) -> None:
    """Placement Readiness Percentage UPDATE SDD §5 "Automatic Updates":
    called after any change to a student's skills/evidence/projects/
    certifications/resume, or their target — recalculates the Skill Gap/
    Placement Readiness analysis immediately if (and only if) a target
    company is already set, so the centralized readiness result never
    goes stale. A no-op when no target is set yet (nothing to recalculate
    against), and also a no-op when the target company doesn't match any
    seeded company intelligence — some callers (e.g. My Profile's Career &
    Placement "Target Company") take free text rather than a company
    picked from `list_company_options`, so an unrecognized name here is
    "no intelligence available yet", not an error worth failing the
    student's actual request over."""
    target_company, target_role = _get_target(db, student_id)
    if not target_company:
        return
    try:
        analyze_skill_gap(db, student_id, target_company, target_role)
    except CompanyNotFoundError:
        pass


def get_placement_readiness_detail(db: Session, student_id: int) -> dict:
    """Student Dashboard UPDATE SDD §11-12 + Student Portal UPDATE SDD §9:
    live-runs Company Intelligence -> Student Skill Analysis -> Placement
    Readiness over the student's *current* stored data — never a stored/
    stale SkillGapAnalysis snapshot — so the "View Detailed Analysis"
    modal always reflects the latest evidence (e.g. right after a resume
    upload) and the currently selected target role. Returns a
    "no analysis" shape (never a fabricated result) when no target
    company is set yet, per the Dependency Condition: an agent may run
    only when its required input actually exists."""
    target_company, target_role = _get_target(db, student_id)
    if target_company is None:
        return {"has_analysis": False}

    company = _get_company_or_raise(db, target_company)
    student = _student_to_dict(db, student_id)
    qdrant = get_client()
    try:
        result = run_student_intelligence_pipeline(
            qdrant, company=_company_to_dict(company), student=student, target_role=target_role
        )
    finally:
        qdrant.close()

    student_analysis = result["student_analysis"]

    return {
        "has_analysis": True,
        "target_company": target_company,
        "target_role": result["company_intel"]["target_role"],
        "readiness_percentage": result["readiness"]["readiness_percentage"],
        "status_message": result["readiness"]["status_message"],
        "current_skills": [
            {
                "skill_name": s["skill_name"],
                "proficiency": s["proficiency"],
                "evidence_count": s["evidence_count"],
            }
            for s in student_analysis["skills"]
        ],
        # The skills the student is genuinely ready with *for this
        # company/role* — the Placement Readiness Agent's own
        # `matched_skills` (meets/exceeds the required proficiency),
        # rather than a company-agnostic evidence heuristic.
        "ready_skills": result["readiness"]["matched_skills"],
    }


def _get_target(db: Session, student_id: int) -> tuple[str | None, str | None]:
    from backend.models.student_profile import StudentCareerPlacement  # noqa: PLC0415

    placement = db.scalar(
        select(StudentCareerPlacement).where(StudentCareerPlacement.student_id == student_id)
    )
    if placement is None:
        return None, None
    return placement.target_company, placement.target_role


def ask_what_if(
    db: Session, student_id: int, company_name: str, target_role: str | None, question: str
) -> WhatIfResult:
    company = _get_company_or_raise(db, company_name)
    student = _student_to_dict(db, student_id)
    qdrant = get_client()
    try:
        result = run_what_if(
            qdrant,
            company=_company_to_dict(company),
            student=student,
            target_role=target_role,
            question=question,
        )
    finally:
        qdrant.close()

    record = WhatIfResult(student_id=student_id, question=question, result=result)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
