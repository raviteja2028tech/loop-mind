"""Student Dashboard aggregation — phase.md Phase 07.

spec.md's Student Portal Dashboard SDD: "The reference layout is fixed;
every student-specific value must be dynamically generated from that
student's actual database/profile data." This module is the single place
that computes all of it, so the route stays a thin pass-through.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.company_intelligence import Company
from backend.models.jobs import JobApplication
from backend.models.preparation import PreparationPlan, StudentProgress
from backend.models.student_profile import (
    StudentAcademicInfo,
    StudentCareerPlacement,
    StudentCertification,
    StudentCodingExperience,
    StudentProfessionalLinks,
    StudentProfile,
    StudentProject,
    StudentSkill,
)
from backend.schemas.dashboard import (
    DashboardOut,
    PlacementReadinessSummary,
    PreparationJourneyStage,
    RecentActivityItem,
    RecommendationCard,
    StatsPoint,
    UpcomingTask,
)
from backend.services import intelligence_service
from backend.services.time_format import relative_time

# spec.md Dashboard §17-20: profile completion is calculated from the
# Student Profile sections that currently exist. Career/Placement,
# Learning/Preparation, Professional Links and Recruitment History are
# defined sections (Phase 04 schema) with no onboarding UI yet (later
# phases) — they aren't counted until a student can actually complete
# them, so this list grows as those phases land rather than capping
# completion below 100% for a reason a student can't act on.
_PROFILE_SECTIONS = 6


def get_target_company(db: Session, student_id: int) -> str | None:
    placement = db.scalar(
        select(StudentCareerPlacement).where(StudentCareerPlacement.student_id == student_id)
    )
    return placement.target_company if placement else None


def set_target_company(db: Session, student_id: int, company_name: str) -> str:
    placement = db.scalar(
        select(StudentCareerPlacement).where(StudentCareerPlacement.student_id == student_id)
    )
    target_role = placement.target_role if placement else None
    if placement is None:
        placement = StudentCareerPlacement(student_id=student_id, target_company=company_name)
        db.add(placement)
    else:
        placement.target_company = company_name
    db.add(
        StudentProgress(
            student_id=student_id,
            event_type="target_company_set",
            event_data={"company_name": company_name},
        )
    )
    db.commit()
    # Placement Readiness Percentage UPDATE SDD §5: changing the target
    # company is one of the listed triggers for an automatic readiness
    # recalculation — refresh immediately rather than leaving the
    # centralized result attached to the *previous* target company.
    intelligence_service.analyze_skill_gap(db, student_id, company_name, target_role)
    return company_name


def list_company_options(db: Session) -> list[str]:
    return sorted(db.scalars(select(Company.name)).all())


_ACTIVITY_LABELS = {
    "basic_info_completed": "Completed Basic Information",
    "academic_info_completed": "Completed Academic Information",
    "skill_added": "Added a new skill",
    "project_added": "Added a new project",
    "certification_added": "Added a certification",
    "target_company_set": "Set a target company",
}
_ACTIVITY_DETAIL_KEYS = {
    "skill_added": "skill_name",
    "project_added": "project_name",
    "certification_added": "certification_name",
    "target_company_set": "company_name",
}


def _recent_activity(db: Session, student_id: int, limit: int = 6) -> list[RecentActivityItem]:
    events = db.scalars(
        select(StudentProgress)
        .where(StudentProgress.student_id == student_id)
        .order_by(StudentProgress.created_at.desc())
        .limit(limit)
    )
    items = []
    for event in events:
        detail_key = _ACTIVITY_DETAIL_KEYS.get(event.event_type)
        items.append(
            RecentActivityItem(
                label=_ACTIVITY_LABELS.get(event.event_type, event.event_type),
                detail=event.event_data.get(detail_key) if detail_key else None,
                relative_time=relative_time(event.created_at),
            )
        )
    return items


def get_dashboard(db: Session, student_id: int) -> DashboardOut:
    profile = db.scalar(select(StudentProfile).where(StudentProfile.student_id == student_id))
    academic = db.scalar(
        select(StudentAcademicInfo).where(StudentAcademicInfo.student_id == student_id)
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
    applications = list(
        db.scalars(select(JobApplication).where(JobApplication.student_id == student_id))
    )
    latest_plan = db.scalar(
        select(PreparationPlan)
        .where(PreparationPlan.student_id == student_id)
        .order_by(PreparationPlan.created_at.desc())
    )
    placement = db.scalar(
        select(StudentCareerPlacement).where(StudentCareerPlacement.student_id == student_id)
    )
    target_company = placement.target_company if placement else None
    target_role = placement.target_role if placement else None
    # Placement Readiness Percentage UPDATE SDD §1/§4: the readiness shown
    # here must be the exact same centralized result the Skill Gap and
    # Preparation Plan pages read — the most recent SkillGapAnalysis for
    # the student's *current* target company, not just "whatever analysis
    # happens to be most recent" (which could be for a target the student
    # has since moved on from).
    latest_gap = (
        intelligence_service.get_latest_skill_gap_analysis(
            db, student_id, target_company, target_role
        )
        if target_company
        else None
    )
    links = db.scalar(
        select(StudentProfessionalLinks).where(StudentProfessionalLinks.student_id == student_id)
    )
    has_resume = bool(links and links.resume_file_path)

    completed_sections = sum(
        [
            profile is not None,
            academic is not None,
            len(skills) > 0,
            len(coding_experience) > 0,
            len(projects) > 0,
            len(certifications) > 0,
        ]
    )
    profile_completion_percentage = round(completed_sections / _PROFILE_SECTIONS * 100)

    if latest_gap is not None:
        readiness = latest_gap.analysis.get("readiness", {})
        placement_readiness = PlacementReadinessSummary(
            has_analysis=True,
            readiness_percentage=readiness.get("readiness_percentage"),
            status_message=readiness.get("status_message"),
        )
    else:
        placement_readiness = PlacementReadinessSummary(has_analysis=False)

    journey = [
        PreparationJourneyStage(
            key="profile",
            label="Profile",
            supporting_text="Build your profile",
            complete=profile_completion_percentage == 100,
        ),
        PreparationJourneyStage(
            key="learn",
            label="Learn",
            supporting_text="Improve skills",
            complete=len(skills) > 0 or len(coding_experience) > 0,
        ),
        PreparationJourneyStage(
            key="apply",
            label="Apply",
            supporting_text="Apply to jobs",
            complete=len(applications) > 0,
        ),
        PreparationJourneyStage(
            key="grow",
            label="Grow",
            supporting_text="Track progress",
            complete=latest_plan is not None,
        ),
    ]

    tasks: list[UpcomingTask] = []
    if academic is None:
        tasks.append(UpcomingTask(label="Complete your profile (Academic Details)"))
    if len(skills) < 2:
        tasks.append(UpcomingTask(label="Add at least 2 skills"))
    if target_company is None:
        tasks.append(UpcomingTask(label="Explore companies"))
    if len(projects) == 0:
        tasks.append(UpcomingTask(label="Add your first project"))
    if len(certifications) == 0:
        tasks.append(UpcomingTask(label="Add a certification"))
    tasks = tasks[:4]

    recommendations: list[RecommendationCard] = []
    if latest_gap is not None:
        for area in latest_gap.analysis.get("skill_gap", {}).get("priority_areas", [])[:4]:
            recommendations.append(
                RecommendationCard(title=f"Learn {area['skill']}", type="Course")
            )
    if len(recommendations) < 4 and len(projects) == 0:
        recommendations.append(
            RecommendationCard(title="Build a Web Project", type="Project Guide")
        )
    if len(recommendations) < 4:
        recommendations.append(RecommendationCard(title="Interview Preparation", type="Resource"))
    if len(recommendations) < 4:
        recommendations.append(RecommendationCard(title="Explore Top Companies", type="Insights"))
    if len(recommendations) < 4:
        recommendations.append(RecommendationCard(title="Complete Your Profile", type="Guide"))
    recommendations = recommendations[:4]

    cutoff = datetime.now(UTC) - timedelta(days=30)

    def _in_window(created_at: datetime) -> bool:
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        return created_at >= cutoff

    stats = [
        StatsPoint(category="Skills", value=sum(1 for s in skills if _in_window(s.created_at))),
        StatsPoint(category="Projects", value=sum(1 for p in projects if _in_window(p.created_at))),
        # No dedicated "learning module" concept exists anywhere in the
        # spec — certifications earned in the window is the one genuinely
        # timestamped, learning-specific signal already on this page
        # (spec.md §22 forbids a fixed 0/placeholder here).
        StatsPoint(
            category="Learning",
            value=sum(1 for c in certifications if _in_window(c.created_at)),
        ),
        StatsPoint(
            category="Applications", value=sum(1 for a in applications if _in_window(a.applied_at))
        ),
    ]

    return DashboardOut(
        full_name=profile.full_name if profile else "Student",
        profile_completion_percentage=profile_completion_percentage,
        skills_count=len(skills),
        projects_count=len(projects),
        certifications_count=len(certifications),
        target_company=target_company,
        has_resume=has_resume,
        placement_readiness=placement_readiness,
        recent_activity=_recent_activity(db, student_id),
        preparation_journey=journey,
        upcoming_tasks=tasks,
        recommended_for_you=recommendations,
        stats=stats,
        updated_at=datetime.now(UTC),
    )
