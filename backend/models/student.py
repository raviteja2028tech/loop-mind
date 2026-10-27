"""Student account record (auth identity only).

The full onboarding profile (Basic Information, Academics, Skills,
Projects, ...) lives in backend/models/student_profile.py, one table per
spec.md Student Profile section, each 1:1 or 1:many with this table.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mobile_number: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    profile = relationship("StudentProfile", back_populates="student", uselist=False)
