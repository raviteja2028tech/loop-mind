"""Student Create Account UPDATE SDD §1/§12: a registration in progress
must never be a real `Student` account. This table is the "temporary/
in-progress registration data" the spec allows — a draft holds everything
the student has entered so far (as nested JSON, one key per onboarding
section, mirroring the existing profile schema) plus any uploaded
photo/resume file paths, keyed by mobile number rather than a student id
because no student exists yet. `registration_service.create_account`
is the only place a real `Student` (and its full profile) ever gets
created from this data — and only after consent — at which point the
draft is deleted.
"""

from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base


def _now() -> datetime:
    return datetime.now(UTC)


class RegistrationDraft(Base):
    __tablename__ = "registration_drafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    mobile_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    otp_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Nested by section: basic_info, academic_info, skills (list),
    # coding_experience, projects (list), certifications (list),
    # career_placement, learning_preparation, professional_links, consent.
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    profile_photo_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resume_file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )
