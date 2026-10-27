from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import CurrentAccount, get_current_account
from backend.core.config import settings
from backend.core.database import get_db
from backend.schemas.auth import (
    AuthSuccessResponse,
    MeResponse,
    SendOtpRequest,
    SendOtpResponse,
    VerifyOtpRequest,
)
from backend.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/send-otp", response_model=SendOtpResponse)
def send_otp(payload: SendOtpRequest, db: Session = Depends(get_db)) -> SendOtpResponse:
    try:
        return auth_service.send_otp(
            db,
            payload.mobile_number,
            payload.purpose,
            dev_mode=settings.environment != "production",
        )
    except auth_service.AccountNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "No account exists with this mobile number."
        ) from exc
    except auth_service.AccountAlreadyExistsError as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "An account has already been created with this mobile number.",
        ) from exc
    except auth_service.OtpCooldownError as exc:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            f"Please wait {exc.retry_after_seconds}s before requesting another code.",
        ) from exc


@router.post("/verify-otp", response_model=AuthSuccessResponse)
def verify_otp(payload: VerifyOtpRequest, db: Session = Depends(get_db)) -> AuthSuccessResponse:
    try:
        return auth_service.verify_otp(db, payload.mobile_number, payload.code, payload.purpose)
    except auth_service.IncorrectOtpError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect OTP, please try again") from exc
    except auth_service.AccountAlreadyExistsError as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "An account has already been created with this mobile number.",
        ) from exc
    except auth_service.AccountNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "No account exists with this mobile number."
        ) from exc


@router.get("/me", response_model=MeResponse)
def me(account: CurrentAccount = Depends(get_current_account)) -> MeResponse:
    return MeResponse(id=account.id, mobile_number=account.mobile_number, role=account.role)
