"""OTP records — spec.md Phase 03 "authentication records".

No expiry/attempt-limit columns: phase.md Phase 03 "Do not invent... OTP
expiry, lockout, attempt limits or resend limits where undefined." Only
the resend cooldown (explicitly specified as 30 seconds) is enforced,
using `created_at`.
"""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base


class OtpRequest(Base):
    __tablename__ = "otp_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mobile_number: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    purpose: Mapped[str] = mapped_column(String(20), nullable=False)  # "login" | "register"
    code_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    consumed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True
    )
