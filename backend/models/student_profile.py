"""Student Profile domain — one table per spec.md Student Profile section.

Schema only (phase.md Phase 04). The onboarding UI/API that populates
these tables is Phase 05 (Skills/Projects/Certifications/Coding
Experience/Evidence) and later phases for Career & Placement, Learning &
Preparation, Professional Links, Recruitment History and Consent, all of
which spec.md's My Profile page (Phase 18) exposes together.

List-like fields (technologies used, skills covered, etc.) are stored as
JSON rather than a fixed enum/table: the source spec explicitly declines
to define closed option lists for most of these ("do not invent a
specific fixed list as user-provided"), so the schema stays open rather
than inventing one.
"""

from datetime import UTC, date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class StudentProfile(Base):
    """Basic Information — spec.md "Create Account -> Basic Information"."""

    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)  # male | female | others
    profile_photo_path: Mapped[str | None] = mapped_column(String(500), nullable=True)  # optional
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    # spec.md My Profile (phase.md Phase 18) Basic Information fields not
    # captured during onboarding (Phase 05) — all optional, filled in later
    # from the profile page itself.
    alternate_mobile_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    current_location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    permanent_location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )

    student = relationship("Student", back_populates="profile")


class StudentAcademicInfo(Base):
    """Academic Information — spec.md "Create Account -> Academic Information"."""

    __tablename__ = "student_academic_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    college: Mapped[str] = mapped_column(String(300), nullable=False)
    # spec.md My Profile "Academic Information": College Location,
    # Specialization — optional, not captured during the original
    # onboarding build pass.
    college_location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    degree: Mapped[str] = mapped_column(String(150), nullable=False)
    branch: Mapped[str] = mapped_column(String(150), nullable=False)
    specialization: Mapped[str | None] = mapped_column(String(150), nullable=True)
    academic_year: Mapped[str] = mapped_column(String(50), nullable=False)
    current_year: Mapped[str] = mapped_column(String(50), nullable=False)
    current_semester: Mapped[str] = mapped_column(String(50), nullable=False)
    admission_year: Mapped[str] = mapped_column(String(10), nullable=False)
    expected_graduation_year: Mapped[str] = mapped_column(String(10), nullable=False)
    current_cgpa: Mapped[float] = mapped_column(nullable=False)
    cgpa_scale: Mapped[str] = mapped_column(String(20), nullable=False)
    # spec.md My Profile "Academic Performance": Academic Percentage —
    # distinct from the 10th/12th scores below, optional.
    academic_percentage: Mapped[float | None] = mapped_column(nullable=True)
    tenth_score_percentage: Mapped[float | None] = mapped_column(nullable=True)  # optional
    twelfth_score_percentage: Mapped[float | None] = mapped_column(nullable=True)  # optional
    # spec.md My Profile "Academic Performance" — not captured during
    # onboarding (Phase 05), optional, filled in later from the profile page.
    semester_wise_sgpa: Mapped[list] = mapped_column(JSON, default=list)
    backlogs: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class StudentSkill(Base):
    """Current Skills — multiple entries allowed, each optionally carrying
    evidence (spec.md "Create Account -> Current Skills")."""

    __tablename__ = "student_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    skill_name: Mapped[str] = mapped_column(String(150), nullable=False)
    skill_category: Mapped[str] = mapped_column(String(100), nullable=False)
    proficiency: Mapped[str] = mapped_column(String(50), nullable=False)
    learning_status: Mapped[str] = mapped_column(String(50), nullable=False)
    experience_years: Mapped[float | None] = mapped_column(nullable=True)
    # Dynamic Resume Replacement & Student Data Synchronization SDD §3-6:
    # "manual" | "resume" | "linkedin" — which extraction (if any) this row
    # came from, so a resume *replacement* can reconcile only the skills it
    # itself previously contributed (removing ones no longer in the new
    # resume) without ever touching a skill the student entered themselves
    # or that came from LinkedIn. Editing a skill by hand marks it
    # "manual" going forward — once a student has touched it, a later
    # resume replacement must not delete it out from under them.
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    evidence = relationship("SkillEvidence", back_populates="skill", cascade="all, delete-orphan")


class SkillEvidence(Base):
    """ "Evidence -> on click -> add project or supporting evidence"; kept
    minimal since the source spec explicitly defers the detailed evidence
    workflow."""

    __tablename__ = "skill_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("student_skills.id"), nullable=False, index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    skill = relationship("StudentSkill", back_populates="evidence")


class StudentCodingExperience(Base):
    """Multiple entries allowed — spec.md "Create Account -> Coding
    Experience": "Multiple coding experience entries are allowed."."""

    __tablename__ = "student_coding_experience"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    coding_experience: Mapped[str | None] = mapped_column(String(100), nullable=True)
    programming_languages: Mapped[list] = mapped_column(JSON, default=list)
    dsa_experience: Mapped[str | None] = mapped_column(String(100), nullable=True)
    competitive_programming: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # beginner | inter-mediate | expert
    coding_platforms: Mapped[list] = mapped_column(JSON, default=list)
    github_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StudentProject(Base):
    """spec.md SDD "PROJECTS" — multiple entries allowed."""

    __tablename__ = "student_projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    project_name: Mapped[str] = mapped_column(String(200), nullable=False)
    project_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    project_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    technologies_used: Mapped[list] = mapped_column(JSON, default=list)
    programming_languages: Mapped[list] = mapped_column(JSON, default=list)
    frameworks: Mapped[list] = mapped_column(JSON, default=list)
    tools: Mapped[list] = mapped_column(JSON, default=list)
    skills_demonstrated: Mapped[list] = mapped_column(JSON, default=list)
    student_role: Mapped[str | None] = mapped_column(String(150), nullable=True)
    team_or_individual: Mapped[str | None] = mapped_column(String(20), nullable=True)
    github_repository: Mapped[str | None] = mapped_column(String(500), nullable=True)
    live_demo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    project_documentation: Mapped[str | None] = mapped_column(String(500), nullable=True)
    project_evidence: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Dynamic Resume Replacement & Student Data Synchronization SDD §3-6 —
    # see StudentSkill.source's docstring above for the full rationale.
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StudentCertification(Base):
    """spec.md SDD "CERTIFICATIONS" — multiple entries allowed."""

    __tablename__ = "student_certifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    certification_name: Mapped[str] = mapped_column(String(200), nullable=False)
    issuing_organization: Mapped[str | None] = mapped_column(String(200), nullable=True)
    certification_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    issue_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    credential_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    credential_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    certificate_file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    skills_covered: Mapped[list] = mapped_column(JSON, default=list)
    # Dynamic Resume Replacement & Student Data Synchronization SDD §3-6 —
    # see StudentSkill.source's docstring above for the full rationale.
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StudentCareerPlacement(Base):
    """spec.md SDD "CAREER / PLACEMENT" (one record per student)."""

    __tablename__ = "student_career_placement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    career_interest: Mapped[str | None] = mapped_column(String(200), nullable=True)
    target_job_role: Mapped[str | None] = mapped_column(String(150), nullable=True)
    preferred_job_domain: Mapped[str | None] = mapped_column(String(150), nullable=True)
    target_company: Mapped[str | None] = mapped_column(String(200), nullable=True)  # optional
    target_role: Mapped[str | None] = mapped_column(String(150), nullable=True)
    preferred_technology_skill_area: Mapped[list] = mapped_column(JSON, default=list)
    placement_interest: Mapped[str | None] = mapped_column(String(50), nullable=True)
    internship_interest: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_job_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_work_location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    preferred_country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    preferred_state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    preferred_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    remote_onsite_hybrid: Mapped[str | None] = mapped_column(String(20), nullable=True)
    preferred_industry: Mapped[str | None] = mapped_column(String(150), nullable=True)
    placement_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class StudentLearningPreparation(Base):
    """spec.md SDD "LEARNING / PREPARATION" (one record per student)."""

    __tablename__ = "student_learning_preparation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    current_learning_areas: Mapped[list] = mapped_column(JSON, default=list)
    skills_currently_learning: Mapped[list] = mapped_column(JSON, default=list)
    learning_goals: Mapped[list] = mapped_column(JSON, default=list)
    areas_to_improve: Mapped[list] = mapped_column(JSON, default=list)
    # phase.md Phase 09 "Your Goals" — structured, individually completable
    # goal items ([{id, text, completed}]), distinct from the free-form
    # `learning_goals` list above. spec.md: "their completion state must be
    # stored dynamically," so these persist rather than living in frontend
    # state.
    short_term_goals: Mapped[list] = mapped_column(JSON, default=list)
    long_term_goals: Mapped[list] = mapped_column(JSON, default=list)
    current_preparation_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    previous_interview_experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    previous_assessment_experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    technical_interview_experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    coding_assessment_experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    interview_preparation_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    assessment_preparation_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class StudentProfessionalLinks(Base):
    """spec.md SDD "PROFESSIONAL LINKS + RESUME" (one record per student)."""

    __tablename__ = "student_professional_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    portfolio_website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    coding_profile_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    other_professional_profile_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resume_file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Recruiter Interview Invitation & Demo Email Specification §5-6: the
    # email address actually found in the student's uploaded resume text —
    # only ever the Email Agent's fallback when `StudentProfile.email` is
    # unavailable, never a substitute source chosen at random. Cleared
    # whenever the resume itself is removed (`delete_resume`), same as
    # `resume_file_path`.
    resume_extracted_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class StudentRecruitmentHistory(Base):
    """spec.md SDD "RECRUITMENT HISTORY + CONSENT" — history half."""

    __tablename__ = "student_recruitment_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    previous_applications: Mapped[str | None] = mapped_column(Text, nullable=True)
    companies_applied_to: Mapped[list] = mapped_column(JSON, default=list)
    roles_applied_to: Mapped[list] = mapped_column(JSON, default=list)
    recruitment_stage_reached: Mapped[str | None] = mapped_column(String(150), nullable=True)
    assessment_participation: Mapped[str | None] = mapped_column(String(150), nullable=True)
    interview_participation: Mapped[str | None] = mapped_column(String(150), nullable=True)
    selection_outcome: Mapped[str | None] = mapped_column(String(150), nullable=True)
    rejection_outcome: Mapped[str | None] = mapped_column(String(150), nullable=True)
    hold_outcome: Mapped[str | None] = mapped_column(String(150), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class StudentConsent(Base):
    """spec.md SDD "RECRUITMENT HISTORY + CONSENT" — consent half."""

    __tablename__ = "student_consent"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True, nullable=False)
    consent_use_information: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_learning_experience: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_anonymized_intelligence: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )
