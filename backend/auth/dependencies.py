"""Authorization dependencies — phase.md Phase 03 "role identification;
authorization". A student must never satisfy a recruiter-only dependency
and vice versa (§"Critical rule")."""

from typing import Literal

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.core.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


class CurrentAccount:
    def __init__(
        self,
        account_id: int,
        role: Literal["student", "recruiter", "registration"],
        mobile_number: str,
    ):
        self.id = account_id
        self.role = role
        self.mobile_number = mobile_number


def get_current_account(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentAccount:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token") from exc
    return CurrentAccount(
        account_id=int(payload["sub"]), role=payload["role"], mobile_number=payload["mobile_number"]
    )


def require_role(role: Literal["student", "recruiter", "registration"]):
    def _dependency(account: CurrentAccount = Depends(get_current_account)) -> CurrentAccount:
        if account.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"{role} access required")
        return account

    return _dependency
