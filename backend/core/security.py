"""JWT + OTP primitives.

spec.md §"FINAL BUILD TECHNOLOGY & AI SPECIFICATION" §3: JWT + OTP
authentication, no password/social auth. phase.md Phase 03 "Do not
invent": no OTP expiry, lockout, or attempt limits where undefined — only
the explicitly-specified 4-digit code and 30-second resend cooldown are
enforced here.
"""

import hashlib
import re
import secrets
from datetime import UTC, datetime, timedelta

import jwt

from backend.core.config import settings

MOBILE_NUMBER_RE = re.compile(r"^\d{10}$")
OTP_RE = re.compile(r"^\d{4}$")
OTP_RESEND_COOLDOWN_SECONDS = 30

# No real SMS provider exists in this environment (spec.md: dev mode returns
# `dev_otp` directly in the API response). Fixed at the user's request so
# every demo login/register always accepts the same code instead of one
# that must be read off the response each time.
DEV_OTP_CODE = "1111"


def is_valid_mobile_number(mobile_number: str) -> bool:
    """spec.md Page 1 SDD §7: "valid 10 digit mobile no."."""
    return bool(MOBILE_NUMBER_RE.match(mobile_number))


def is_valid_otp_format(code: str) -> bool:
    """spec.md: OTP is exactly 4 digits."""
    return bool(OTP_RE.match(code))


def generate_otp() -> str:
    return f"{secrets.randbelow(10_000):04d}"


def hash_otp(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def create_access_token(*, account_id: int, role: str, mobile_number: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload = {
        "sub": str(account_id),
        "role": role,
        "mobile_number": mobile_number,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
