"""Preparation Plan page aggregation — phase.md Phase 09.

Turns the stored *current* PreparationPlan (Phase 06's generate/store
action, reused as-is here) into the exact Year-Wise Focus / Your Goals /
AI Recommendations / Detailed Preparation Plan structure the reference
layout requires — cross-referencing the student's live skills and the
target role's live requirements for Current/Target Level, the same way
the Skill Gap page does, so both pages agree on what a skill's status is.
"""

import uuid
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.preparation import PreparationPlan
from backend.models.student_profile import StudentAcademicInfo, StudentLearningPreparation
from backend.schemas.preparation_plan_page import (
    GoalOut,
    PlanRowOut,
    PreparationPlanPageOut,
    ReadinessSummaryOut,
    RecommendationOut,
    YearFocusOut,
)
from backend.services import intelligence_service
from backend.services import skill_gap_page_service as skill_gap
from backend.services.dashboard_service import list_company_options
from backend.services.skill_lookup import category_for, required_levels_for, student_skill_lookup

ACADEMIC_YEAR_OPTIONS = ["1st Year", "2nd Year", "3rd Year", "Final Year"]

# Mirrors AI services/agents/preparation_plan_agent.py's _YEAR_EMPHASIS
# guidance text — this module only needs the display text, not the
# horizon it also returns (each plan item already carries its own).
_YEAR_FOCUS = {
    "1st Year": "Focus on fundamentals, broad learning, and building initial evidence.",
    "2nd Year": "Deepen skills and ship more substantial projects.",
    "3rd Year": "Prioritize company-focused skills, DSA, and interview preparation.",
    "Final Year": "Focus tightly on placement-ready, company-specific preparation.",
}

_HORIZON_DAYS = {"short-term": 30, "medium-term": 60, "long-term": 90}


def _filter_category_for(skill: str, item_category: str) -> str:
    """Maps a plan item onto spec.md's fixed 7 filter-tab categories (All/
    DSA/Development/System Design/Databases/Interview Prep/Projects/
    Other) — the tabs themselves are fixed by the reference layout, only
    which bucket a given real skill lands in is dynamic."""
    if item_category == "Evidence":
        return "Projects"
    lowered = skill.strip().lower()
    if "data structures" in lowered or "algorithm" in lowered or lowered == "dsa":
        return "DSA"
    if "system design" in lowered:
        return "System Design"
    if "sql" in lowered or "database" in lowered:
        return "Databases"
    if category_for(skill) != "General":
        return "Development"
    return "Other"


def _get_or_create_learning(db: Session, student_id: int) -> StudentLearningPreparation:
    row = db.scalar(
        select(StudentLearningPreparation).where(
            StudentLearningPreparation.student_id == student_id
        )
    )
    if row is None:
        row = StudentLearningPreparation(student_id=student_id)
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


def _goal_field(kind: str) -> str:
    return "short_term_goals" if kind == "short_term" else "long_term_goals"


def list_goals(db: Session, student_id: int) -> tuple[list[GoalOut], list[GoalOut]]:
    row = _get_or_create_learning(db, student_id)
    return (
        [GoalOut(**g) for g in row.short_term_goals],
        [GoalOut(**g) for g in row.long_term_goals],
    )


def add_goal(
    db: Session, student_id: int, kind: str, text: str
) -> tuple[list[GoalOut], list[GoalOut]]:
    row = _get_or_create_learning(db, student_id)
    field = _goal_field(kind)
    goals = [*getattr(row, field), {"id": uuid.uuid4().hex[:8], "text": text, "completed": False}]
    setattr(row, field, goals)
    db.commit()
    return list_goals(db, student_id)


def toggle_goal(
    db: Session, student_id: int, kind: str, goal_id: str
) -> tuple[list[GoalOut], list[GoalOut]]:
    row = _get_or_create_learning(db, student_id)
    field = _goal_field(kind)
    goals = [dict(g) for g in getattr(row, field)]
    for goal in goals:
        if goal["id"] == goal_id:
            goal["completed"] = not goal["completed"]
    setattr(row, field, goals)
    db.commit()
    return list_goals(db, student_id)


def _readiness_summary(
    db: Session, student_id: int, target_company: str | None, target_role: str | None
) -> ReadinessSummaryOut:
    # Placement Readiness Percentage UPDATE SDD §3/§4: Current Readiness
    # here must be the exact same centralized result as Dashboard's
    # Placement Readiness and Skill Gap's Overall Readiness — reusing the
    # one shared, auto-creating lookup keeps all three consistent
    # regardless of which page the student happens to visit first.
    if target_company is None:
        return ReadinessSummaryOut(has_analysis=False)
    latest = intelligence_service.get_latest_skill_gap_analysis(
        db, student_id, target_company, target_role
    )
    readiness = latest.analysis["readiness"]
    return ReadinessSummaryOut(
        has_analysis=True,
        readiness_percentage=readiness["readiness_percentage"],
        status_message=readiness["status_message"],
    )


def _plan_rows(db: Session, student_id: int, plan: PreparationPlan) -> list[PlanRowOut]:
    """Student Portal Preparation Plan UPDATE SDD §5-9: the roadmap is a
    continuous chronological sequence, not every skill sharing the same
    start/end window — each item's window begins the day after the
    previous item's window ends, in the same priority order the
    Preparation Plan Agent already produced (highest-priority skill
    learned first)."""
    required_levels = (
        required_levels_for(db, plan.target_company, plan.target_role)
        if plan.target_company
        else {}
    )
    student_lookup = student_skill_lookup(db, student_id)
    next_start = plan.created_at.date()

    rows = []
    for item in plan.plan.get("items", []):
        skill = item["skill"]
        key = skill.strip().lower()
        category, current_level = student_lookup.get(key, (category_for(skill), "Not Started"))
        target_level = required_levels.get(key, "—")
        status = "Missing" if current_level == "Not Started" else "To Improve"
        days = _HORIZON_DAYS.get(item.get("horizon", ""), 60)
        start = next_start
        end = start + timedelta(days=days)
        next_start = end + timedelta(days=1)
        rows.append(
            PlanRowOut(
                skill=skill,
                category=category,
                filter_category=_filter_category_for(skill, item.get("category", "")),
                current_level=current_level,
                target_level=target_level,
                start_date=start,
                end_date=end,
                status=status,
                priority=item["priority"],
                resources=item["action"],
            )
        )
    return rows


def _recommendations_for(rows: list[PlanRowOut]) -> list[RecommendationOut]:
    recs = [RecommendationOut(title=row.resources) for row in rows[:5]]
    fallbacks = [
        "Keep your skills profile up to date so recommendations stay accurate.",
        "Revisit your target company and role as your profile grows.",
        "Add project evidence for the skills you already have.",
        "Check the Skill Gap page for a detailed breakdown of your readiness.",
        "Set a target company to unlock personalized recommendations.",
    ]
    i = 0
    while len(recs) < 5 and i < len(fallbacks):
        recs.append(RecommendationOut(title=fallbacks[i]))
        i += 1
    return recs[:5]


def get_page(db: Session, student_id: int) -> PreparationPlanPageOut:
    target_company, target_role = skill_gap.get_target(db, student_id)
    academic = db.scalar(
        select(StudentAcademicInfo).where(StudentAcademicInfo.student_id == student_id)
    )
    academic_year = academic.current_year if academic else None

    company_options = list_company_options(db)
    role_options = skill_gap.list_role_options(db, target_company) if target_company else []

    year_wise_focus = [
        YearFocusOut(year=year, focus_text=focus, is_current=year == academic_year)
        for year, focus in _YEAR_FOCUS.items()
    ]

    short_term, long_term = list_goals(db, student_id)

    latest_plan = None
    if target_company:
        latest_plan = db.scalar(
            select(PreparationPlan)
            .where(
                PreparationPlan.student_id == student_id,
                PreparationPlan.target_company == target_company,
                PreparationPlan.status == "current",
            )
            .order_by(PreparationPlan.created_at.desc())
        )

    plan_rows = _plan_rows(db, student_id, latest_plan) if latest_plan else []

    return PreparationPlanPageOut(
        target_company=target_company,
        target_role=target_role,
        academic_year=academic_year,
        company_options=company_options,
        role_options=role_options,
        academic_year_options=ACADEMIC_YEAR_OPTIONS,
        readiness=_readiness_summary(db, student_id, target_company, target_role),
        year_wise_focus=year_wise_focus,
        short_term_goals=short_term,
        long_term_goals=long_term,
        recommendations=_recommendations_for(plan_rows),
        has_plan=latest_plan is not None,
        plan_version=latest_plan.version if latest_plan else None,
        plan_status=latest_plan.status if latest_plan else None,
        plan_items=plan_rows,
    )


def generate_plan(
    db: Session,
    student_id: int,
    company_name: str,
    target_role: str | None,
    academic_year: str | None,
) -> PreparationPlanPageOut:
    skill_gap.set_target(db, student_id, company_name, target_role)
    intelligence_service.generate_preparation_plan(
        db, student_id, company_name, target_role, academic_year_override=academic_year
    )
    return get_page(db, student_id)
