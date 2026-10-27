"""Development/demo data seeding.

spec.md "Recruiter Account — Development/Demo Requirement": a demo
Recruiter account must exist so the full auth flow (mobile -> OTP ->
Recruiter Portal) can be tested end-to-end before real recruiter
onboarding (Phase 11) exists. Only runs outside production.

A demo Student account is seeded on the same basis, purely so the
student-side Login path (an existing account) is demonstrable without
first running Create Account — it carries no profile data, so its
dashboard still shows the same honest zero-state a real new student
would see; phase.md forbids fabricating activity/profile data.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.recruiter import Recruiter
from backend.models.student import Student

DEMO_RECRUITER_MOBILE = "9999999999"
DEMO_STUDENT_MOBILE = "8888888888"


def seed_demo_recruiter(db: Session) -> None:
    exists = db.scalar(select(Recruiter).where(Recruiter.mobile_number == DEMO_RECRUITER_MOBILE))
    if exists is None:
        db.add(Recruiter(mobile_number=DEMO_RECRUITER_MOBILE, name="Demo Recruiter"))
        db.commit()


def seed_demo_student(db: Session) -> None:
    exists = db.scalar(select(Student).where(Student.mobile_number == DEMO_STUDENT_MOBILE))
    if exists is None:
        db.add(Student(mobile_number=DEMO_STUDENT_MOBILE))
        db.commit()
