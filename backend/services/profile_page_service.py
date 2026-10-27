"""My Profile page aggregation — phase.md Phase 18.

Everything here reads the authenticated student's own stored rows only —
spec.md §26 "Dynamic Data Rule": never a hardcoded name/percentage/count.
`get_recruitment_history` derives its answer from the real
`JobApplication`/`Interview`/`HumanApproval` rows Phases 10-16 created,
rather than the separate hand-entered `StudentRecruitmentHistory` table —
see backend/schemas/profile_page.py's module docstring for why.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.jobs import JobApplication
from backend.models.student_profile import StudentAcademicInfo, StudentProfile
from backend.schemas.profile_page import (
    MissingFieldOut,
    ProfileOverviewOut,
    ProfilePageOut,
    ProfileStatsOut,
    RecruitmentApplicationOut,
    RecruitmentHistoryOut,
)
from backend.services import student_profile_service as profile_service
from backend.services.time_format import relative_time

# spec.md §7 "Profile Completion": the percentage must be dynamically
# calculated, never hardcoded. This page's own definition is deliberately
# broader than the Student Dashboard's (Phase 07) — Career & Placement,
# Learning & Preparation, Professional Links and Consent only gained an
# editing UI in this phase, so only *this* page's completion counts them;
# the Dashboard's existing, already-tested metric is left untouched.
_SECTION_COUNT = 10


def _missing_fields(
    profile: StudentProfile | None,
    academic: StudentAcademicInfo | None,
    has_skills: bool,
    has_projects: bool,
    has_certifications: bool,
    career,
    learning,
    links,
    consent,
    has_coding_experience: bool,
) -> list[MissingFieldOut]:
    missing = []
    if profile is None:
        missing.append(MissingFieldOut(section="Basic Information", field="All fields"))
    if academic is None:
        missing.append(MissingFieldOut(section="Academics", field="All fields"))
    if not has_skills:
        missing.append(MissingFieldOut(section="Skills", field="At least one skill"))
    if not has_coding_experience:
        missing.append(MissingFieldOut(section="Coding Experience", field="At least one entry"))
    if not has_projects:
        missing.append(MissingFieldOut(section="Projects", field="At least one project"))
    if not has_certifications:
        missing.append(
            MissingFieldOut(section="Certifications", field="At least one certification")
        )
    if career is None or not career.target_company:
        missing.append(MissingFieldOut(section="Career & Placement", field="Target Company"))
    if learning is None or not learning.current_preparation_status:
        missing.append(
            MissingFieldOut(section="Learning & Preparation", field="Current Preparation Status")
        )
    if links is None or not links.resume_file_path:
        missing.append(MissingFieldOut(section="Professional Links & Resume", field="Resume"))
    if consent is None:
        missing.append(MissingFieldOut(section="Consent & Knowledge Sharing", field="All consents"))
    return missing


def get_profile_page(db: Session, student_id: int) -> ProfilePageOut:
    profile = profile_service.get_basic_info(db, student_id)
    academic = profile_service.get_academic_info(db, student_id)
    skills = profile_service.list_skills(db, student_id)
    coding_experience = profile_service.list_coding_experience(db, student_id)
    projects = profile_service.list_projects(db, student_id)
    certifications = profile_service.list_certifications(db, student_id)
    career = profile_service.get_career_placement(db, student_id)
    learning = profile_service.get_learning_preparation(db, student_id)
    links = profile_service.get_professional_links(db, student_id)
    consent = profile_service.get_consent(db, student_id)
    applications = list(
        db.scalars(select(JobApplication).where(JobApplication.student_id == student_id))
    )

    completed_sections = sum(
        [
            profile is not None,
            academic is not None,
            len(skills) > 0,
            len(coding_experience) > 0,
            len(projects) > 0,
            len(certifications) > 0,
            career is not None and bool(career.target_company),
            learning is not None and bool(learning.current_preparation_status),
            links is not None and bool(links.resume_file_path),
            consent is not None,
        ]
    )
    completion_percentage = round(completed_sections / _SECTION_COUNT * 100)

    overview = ProfileOverviewOut(
        full_name=profile.full_name if profile else None,
        degree=academic.degree if academic else None,
        college=academic.college if academic else None,
        current_semester=academic.current_semester if academic else None,
        city=profile.city if profile else None,
        state=profile.state if profile else None,
        profile_photo_path=profile.profile_photo_path if profile else None,
        has_resume=bool(links and links.resume_file_path),
    )

    return ProfilePageOut(
        overview=overview,
        completion_percentage=completion_percentage,
        missing_fields=_missing_fields(
            profile,
            academic,
            len(skills) > 0,
            len(projects) > 0,
            len(certifications) > 0,
            career,
            learning,
            links,
            consent,
            len(coding_experience) > 0,
        ),
        stats=ProfileStatsOut(
            skills_added=len(skills),
            projects=len(projects),
            certifications=len(certifications),
            job_applications=len(applications),
        ),
    )


def get_recruitment_history(db: Session, student_id: int) -> RecruitmentHistoryOut:
    applications = list(
        db.scalars(
            select(JobApplication)
            .where(JobApplication.student_id == student_id)
            .order_by(JobApplication.applied_at.desc())
        )
    )

    rows = []
    selected = rejected = hold = 0
    for application in applications:
        approval = application.approval
        interview = application.interview
        outcome = None
        if interview and interview.outcome == "hired":
            stage, outcome = "Hired", "Hired"
            selected += 1
        elif interview and interview.outcome == "not_selected":
            stage, outcome = "Not Selected", "Not Selected"
            rejected += 1
        elif approval and approval.decision == "disapproved":
            stage, outcome = "Disapproved", "Disapproved"
            rejected += 1
        elif approval and approval.decision == "approved":
            stage = "Interview" if interview else "Approved"
            hold += 1
        elif application.match_result and application.match_result.ai_status == "shortlisted":
            stage = "AI Shortlisted"
            hold += 1
        else:
            stage = "Under Review"
            hold += 1

        rows.append(
            RecruitmentApplicationOut(
                company_name=application.job.company_name,
                job_role=application.job.job_role,
                applied_relative=relative_time(application.applied_at),
                recruitment_stage_reached=stage,
                outcome=outcome,
            )
        )

    return RecruitmentHistoryOut(
        total_applications=len(applications),
        companies_applied_to=sorted({a.job.company_name for a in applications}),
        roles_applied_to=sorted({a.job.job_role for a in applications}),
        selected_count=selected,
        rejected_count=rejected,
        hold_count=hold,
        applications=rows,
    )
