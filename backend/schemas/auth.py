from typing import Literal

from pydantic import BaseModel, field_validator

from backend.core.security import is_valid_mobile_number, is_valid_otp_format

Purpose = Literal["login", "register"]


class SendOtpRequest(BaseModel):
    mobile_number: str
    purpose: Purpose

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        if not is_valid_mobile_number(v):
            raise ValueError("mobile_number must be exactly 10 digits")
        return v


class SendOtpResponse(BaseModel):
    mobile_number: str
    resend_available_in_seconds: int
    # Present only outside production — spec.md explicitly defers a real
    # SMS provider; this is the honest stand-in so the flow is testable.
    dev_otp: str | None = None


class VerifyOtpRequest(BaseModel):
    mobile_number: str
    code: str
    purpose: Purpose

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        if not is_valid_mobile_number(v):
            raise ValueError("mobile_number must be exactly 10 digits")
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not is_valid_otp_format(v):
            raise ValueError("code must be exactly 4 digits")
        return v


class AuthSuccessResponse(BaseModel):
    token: str
    # "registration" — Student Create Account UPDATE SDD §1/§3/§12: OTP
    # verification issues a registration-draft token, never a real student
    # account, until Create Account succeeds.
    role: Literal["student", "recruiter", "registration"]
    redirect: str


class MeResponse(BaseModel):
    id: int
    mobile_number: str
    role: Literal["student", "recruiter", "registration"]
