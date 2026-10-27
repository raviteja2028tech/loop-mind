from datetime import date

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.database import Base
from backend.core.seed import DEMO_RECRUITER_MOBILE, seed_demo_recruiter
from backend.core.seed_company_intelligence import seed_company_intelligence
from backend.models import (
    Company,
    CompanyRoleRequirement,
    Job,
    JobApplication,
    PreparationPlan,
    Recruiter,
    SkillEvidence,
    Student,
    StudentProfile,
    StudentSkill,
)


def _session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_all_tables_created_without_error():
    db = _session()
    # A representative table from each domain must exist and be queryable.
    for model in (
        Student,
        Recruiter,
        StudentProfile,
        StudentSkill,
        Job,
        JobApplication,
        PreparationPlan,
        Company,
        CompanyRoleRequirement,
    ):
        assert db.scalar(select(model).limit(1)) is None  # empty, but no schema error


def test_student_profile_and_skill_relationships():
    db = _session()
    student = Student(mobile_number="9876500001")
    db.add(student)
    db.flush()

    db.add(
        StudentProfile(
            student_id=student.id,
            full_name="Test Student",
            date_of_birth=date(2003, 5, 1),
            gender="female",
            email="test.student@example.com",
            country="India",
            state="Karnataka",
            city="Bengaluru",
        )
    )
    skill = StudentSkill(
        student_id=student.id,
        skill_name="Python",
        skill_category="Programming Language",
        proficiency="Intermediate",
        learning_status="Learning",
    )
    db.add(skill)
    db.flush()
    db.add(SkillEvidence(skill_id=skill.id, description="Built a Django project", link=None))
    db.commit()

    fetched_student = db.scalar(select(Student).where(Student.mobile_number == "9876500001"))
    assert fetched_student.profile.full_name == "Test Student"

    fetched_skill = db.scalar(select(StudentSkill).where(StudentSkill.student_id == student.id))
    assert fetched_skill.evidence[0].description == "Built a Django project"


def test_job_application_chain():
    db = _session()
    recruiter = Recruiter(mobile_number="9000000001")
    student = Student(mobile_number="9876500002")
    db.add_all([recruiter, student])
    db.flush()

    job = Job(
        recruiter_id=recruiter.id,
        company_name="Test Company",
        job_title="Software Engineer",
        job_role="Backend",
        experience_required="0-2 years",
    )
    db.add(job)
    db.flush()

    application = JobApplication(job_id=job.id, student_id=student.id)
    db.add(application)
    db.commit()

    fetched_job = db.scalar(select(Job).where(Job.id == job.id))
    assert len(fetched_job.applications) == 1
    assert fetched_job.applications[0].student_id == student.id


def test_company_intelligence_seed_is_populated_and_idempotent():
    db = _session()
    seed_company_intelligence(db)

    companies = db.scalars(select(Company)).all()
    assert len(companies) >= 10
    assert all(c.is_synthetic for c in companies)

    role_requirements = db.scalars(select(CompanyRoleRequirement)).all()
    assert len(role_requirements) >= len(companies)
    for req in role_requirements:
        assert len(req.required_skills) > 0

    # Idempotent: calling again must not duplicate.
    seed_company_intelligence(db)
    companies_after = db.scalars(select(Company)).all()
    assert len(companies_after) == len(companies)


def test_demo_recruiter_seed_is_idempotent():
    db = _session()
    seed_demo_recruiter(db)
    seed_demo_recruiter(db)
    recruiters = db.scalars(
        select(Recruiter).where(Recruiter.mobile_number == DEMO_RECRUITER_MOBILE)
    ).all()
    assert len(recruiters) == 1


def test_preparation_plan_versioning_columns():
    db = _session()
    student = Student(mobile_number="9876500003")
    db.add(student)
    db.flush()

    db.add(
        PreparationPlan(
            student_id=student.id,
            target_company="Nexora Technologies",
            version=1,
            status="historical",
            plan={"items": []},
        )
    )
    db.add(
        PreparationPlan(
            student_id=student.id,
            target_company="Nexora Technologies",
            version=2,
            status="current",
            plan={"items": ["DSA"]},
        )
    )
    db.commit()

    plans = db.scalars(
        select(PreparationPlan)
        .where(PreparationPlan.student_id == student.id)
        .order_by(PreparationPlan.version)
    ).all()
    assert [p.version for p in plans] == [1, 2]
    assert plans[-1].status == "current"
