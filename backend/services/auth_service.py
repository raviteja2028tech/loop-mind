"""Authentication business logic.

Implements spec.md's confirmed authentication requirement:

    CREATE ACCOUNT               LOGIN
    Enter mobile                 Enter mobile
    Check database                Check database
    EXISTS -> "Account            EXISTS -> send OTP -> verify -> continue
      Already Exists" -> Login    NEW     -> "Account Not Found" -> Register
    NEW -> send OTP -> verify -> continue

and the resend rule: "OTP sent -> 30-second waiting period -> Resend code
becomes active." No expiry/attempt-limit is implemented — see
backend/core/security.py.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.security import (
    DEV_OTP_CODE,
    OTP_RESEND_COOLDOWN_SECONDS,
    create_access_token,
    generate_otp,
    hash_otp,
)
from backend.models.otp_request import OtpRequest
from backend.models.recruiter import Recruiter
from backend.models.registration_draft import RegistrationDraft
from backend.models.student import Student
from backend.schemas.auth import AuthSuccessResponse, Purpose, SendOtpResponse


class AccountNotFoundError(Exception):
    """Login attempted for a mobile number with no registered account."""


class AccountAlreadyExistsError(Exception):
    """Register attempted for a mobile number that already has an account."""


class OtpCooldownError(Exception):
    def __init__(self, retry_after_seconds: int):
        self.retry_after_seconds = retry_after_seconds


class IncorrectOtpError(Exception):
    """spec.md: "Incorrect OTP, please try again"."""


def _find_account(db: Session, mobile_number: str) -> tuple[Student | Recruiter | None, str | None]:
    student = db.scalar(select(Student).where(Student.mobile_number == mobile_number))
    if student:
        return student, "student"
    recruiter = db.scalar(select(Recruiter).where(Recruiter.mobile_number == mobile_number))
    if recruiter:
        return recruiter, "recruiter"
    return None, None


def send_otp(
    db: Session, mobile_number: str, purpose: Purpose, *, dev_mode: bool
) -> SendOtpResponse:
    account, _ = _find_account(db, mobile_number)

    if purpose == "login" and account is None:
        raise AccountNotFoundError()
    if purpose == "register" and account is not None:
        raise AccountAlreadyExistsError()

    cutoff = datetime.now(UTC) - timedelta(seconds=OTP_RESEND_COOLDOWN_SECONDS)
    last = db.scalar(
        select(OtpRequest)
        .where(OtpRequest.mobile_number == mobile_number, OtpRequest.purpose == purpose)
        .order_by(OtpRequest.created_at.desc())
    )
    if last is not None:
        last_created = last.created_at
        if last_created.tzinfo is None:
            last_created = last_created.replace(tzinfo=UTC)
        if last_created > cutoff:
            retry_after = OTP_RESEND_COOLDOWN_SECONDS - int(
                (datetime.now(UTC) - last_created).total_seconds()
            )
            raise OtpCooldownError(max(retry_after, 1))

    code = DEV_OTP_CODE if dev_mode else generate_otp()
    db.add(OtpRequest(mobile_number=mobile_number, purpose=purpose, code_hash=hash_otp(code)))
    db.commit()

    return SendOtpResponse(
        mobile_number=mobile_number,
        resend_available_in_seconds=OTP_RESEND_COOLDOWN_SECONDS,
        dev_otp=code if dev_mode else None,
    )


def verify_otp(db: Session, mobile_number: str, code: str, purpose: Purpose) -> AuthSuccessResponse:
    otp_request = db.scalar(
        select(OtpRequest)
        .where(
            OtpRequest.mobile_number == mobile_number,
            OtpRequest.purpose == purpose,
            OtpRequest.consumed.is_(False),
        )
        .order_by(OtpRequest.created_at.desc())
    )
    if otp_request is None or otp_request.code_hash != hash_otp(code):
        raise IncorrectOtpError()

    otp_request.consumed = True

    if purpose == "register":
        account, _ = _find_account(db, mobile_number)
        if account is not None:
            raise AccountAlreadyExistsError()

        # Student Create Account UPDATE SDD §1/§3/§12: OTP verification
        # must never create the real account — only a temporary
        # registration draft, resumed rather than duplicated if the
        # student already started (and abandoned mid-flow) once before.
        draft = db.scalar(
            select(RegistrationDraft).where(RegistrationDraft.mobile_number == mobile_number)
        )
        if draft is None:
            draft = RegistrationDraft(mobile_number=mobile_number)
            db.add(draft)
        db.commit()
        db.refresh(draft)
        token = create_access_token(
            account_id=draft.id, role="registration", mobile_number=mobile_number
        )
        db.commit()
        return AuthSuccessResponse(token=token, role="registration", redirect="/app")

    # purpose == "login"
    account, role = _find_account(db, mobile_number)
    if account is None or role is None:
        raise AccountNotFoundError()
    db.commit()
    token = create_access_token(account_id=account.id, role=role, mobile_number=mobile_number)
    redirect = "/app" if role == "student" else "/recruiter"
    return AuthSuccessResponse(token=token, role=role, redirect=redirect)  # type: ignore[arg-type]
