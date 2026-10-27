"""Skill Gap Analysis page aggregation — phase.md Phase 08.

spec.md's Skill Gap Analysis SDD: "The reference layout is fixed; every
value must be dynamically calculated." This module turns the Phase 06
multi-agent pipeline's stored analysis (existing/weak/missing/not-relevant
skill name lists + priority areas + readiness) into the exact cards/table
the page needs, cross-referencing the student's *current* skills and the
target role's *current* requirements so displayed levels always reflect
live data rather than a stale snapshot from whenever the analysis last ran.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.company_intelligence import Company
from backend.models.student_profile import StudentCareerPlacement
from backend.schemas.skill_gap import (
    PriorityAreaOut,
    ReadinessOut,
    SkillDistributionOut,
    SkillGapOverviewOut,
    SkillGapPageOut,
    SkillRowOut,
)
from backend.services import intelligence_service
from backend.services.dashboard_service import list_company_options
from backend.services.skill_lookup import (
    category_for,
    required_levels_for,
    student_skill_lookup,
)

_IMPACT_LABEL = {"High": "High Impact", "Medium": "Medium Impact", "Low": "Low Impact"}


def _resource_action_for(skill: str, priority: str, target_company: str) -> str:
    """Mirrors the Preparation Plan Agent's per-priority action text (AI
    services/agents/preparation_plan_agent.py) — the same genuinely
    skill-specific guidance, reused here as the "View Resources" content
    rather than a fabricated external links catalog."""
    if priority == "High":
        return f"Learn {skill} from the ground up and build a small project using it."
    if priority == "Medium":
        return f"Strengthen {skill} toward the level {target_company} expects."
    return f"Attach a project or certification link as evidence for {skill}."


def get_target(db: Session, student_id: int) -> tuple[str | None, str | None]:
    placement = db.scalar(
        select(StudentCareerPlacement).where(StudentCareerPlacement.student_id == student_id)
    )
    if placement is None:
        return None, None
    return placement.target_company, placement.target_role


def set_target(db: Session, student_id: int, company_name: str, target_role: str | None) -> None:
    placement = db.scalar(
        select(StudentCareerPlacement).where(StudentCareerPlacement.student_id == student_id)
    )
    if placement is None:
        placement = StudentCareerPlacement(
            student_id=student_id, target_company=company_name, target_role=target_role
        )
        db.add(placement)
    else:
        placement.target_company = company_name
        placement.target_role = target_role
    db.commit()


def list_role_options(db: Session, company_name: str) -> list[str]:
    company = db.scalar(select(Company).where(Company.name == company_name))
    if company is None:
        return []
    return sorted({r.role_title for r in company.role_requirements})


def _empty_page(company_options: list[str]) -> SkillGapPageOut:
    return SkillGapPageOut(
        target_company=None,
        target_role=None,
        company_options=company_options,
        role_options=[],
        readiness=ReadinessOut(has_analysis=False),
        overview=SkillGapOverviewOut(
            total_required_skills=0, skills_you_have=0, skills_to_improve=0, missing_evidence=0
        ),
        distribution=SkillDistributionOut(
            already_strong=0, needs_improvement=0, missing=0, not_relevant=0
        ),
        priority_areas=[],
        skills=[],
    )


def get_skill_gap_page(db: Session, student_id: int) -> SkillGapPageOut:
    target_company, target_role = get_target(db, student_id)
    company_options = list_company_options(db)

    if target_company is None:
        return _empty_page(company_options)

    role_options = list_role_options(db, target_company)

    # Placement Readiness Percentage UPDATE SDD §4 "Single Source of
    # Truth": always go through the shared lookup (also used by Dashboard
    # and Preparation Plan) rather than a page-local query, so this page's
    # Overall Readiness can never diverge from theirs.
    latest = intelligence_service.get_latest_skill_gap_analysis(
        db, student_id, target_company, target_role
    )

    gap = latest.analysis["skill_gap"]
    readiness_data = latest.analysis["readiness"]
    resolved_role = latest.target_role

    required_levels = required_levels_for(db, target_company, resolved_role)
    student_lookup = student_skill_lookup(db, student_id)

    missing_evidence_names = set(gap["missing_evidence"])

    def _row(name: str, status: str) -> SkillRowOut:
        key = name.strip().lower()
        category, your_level = student_lookup.get(key, (category_for(name), "Not Started"))
        required_level = required_levels.get(key, "—")
        priority_entry = next((p for p in gap["priority_areas"] if p["skill"] == name), None)
        priority = priority_entry["priority"] if priority_entry else None
        resources = _resource_action_for(name, priority, target_company) if priority else None
        # spec.md UPDATE — Student Portal Skill Gap SDD §6: a skill that
        # meets the required level but has no supporting evidence must be
        # represented as "Missing Evidence" in the table, not silently
        # shown as fully verified "Strong" (it still counts toward the
        # Missing Evidence overview number — this makes the per-row
        # status agree with that count).
        if status == "Strong" and name in missing_evidence_names:
            status = "Missing Evidence"
        return SkillRowOut(
            skill=name,
            category=category,
            your_level=your_level,
            required_level=required_level,
            status=status,
            priority=priority,
            resources=resources,
        )

    rows = (
        [_row(n, "Strong") for n in gap["existing_skills"]]
        + [_row(n, "To Improve") for n in gap["weak_skills"]]
        + [_row(n, "Missing") for n in gap["missing_skills"]]
        + [_row(n, "Not Relevant") for n in gap["not_relevant_skills"]]
    )

    total_required = (
        len(gap["existing_skills"]) + len(gap["weak_skills"]) + len(gap["missing_skills"])
    )

    priority_areas_out = [
        PriorityAreaOut(
            rank=i + 1, skill=p["skill"], impact=_IMPACT_LABEL.get(p["priority"], "Medium Impact")
        )
        for i, p in enumerate(gap["priority_areas"][:5])
    ]

    return SkillGapPageOut(
        target_company=target_company,
        target_role=resolved_role,
        company_options=company_options,
        role_options=role_options,
        readiness=ReadinessOut(
            has_analysis=True,
            readiness_percentage=readiness_data["readiness_percentage"],
            status_message=readiness_data["status_message"],
            supporting_text=gap.get("reasoning"),
        ),
        overview=SkillGapOverviewOut(
            total_required_skills=total_required,
            # Skill Gap/Profile Photo/Resume Management UPDATE SDD §1: this
            # is the student's *own* current skill count (deduped, from
            # every source already merged into StudentSkill — resume,
            # profile entry, LinkedIn), not "how many required skills they
            # happen to already meet" (`existing_skills`, which is what
            # the Already Strong distribution bucket below correctly
            # measures) — those are two different questions and the
            # former must never read as 0 just because none of a
            # student's real skills overlap with this particular target's
            # required list.
            skills_you_have=len(student_lookup),
            skills_to_improve=len(gap["weak_skills"]),
            missing_evidence=len(gap["missing_evidence"]),
        ),
        distribution=SkillDistributionOut(
            already_strong=len(gap["existing_skills"]),
            needs_improvement=len(gap["weak_skills"]),
            missing=len(gap["missing_skills"]),
            not_relevant=len(gap["not_relevant_skills"]),
        ),
        priority_areas=priority_areas_out,
        skills=rows,
    )


def set_target_and_refresh(
    db: Session, student_id: int, company_name: str, target_role: str | None
) -> SkillGapPageOut:
    set_target(db, student_id, company_name, target_role)
    intelligence_service.analyze_skill_gap(db, student_id, company_name, target_role)
    return get_skill_gap_page(db, student_id)
