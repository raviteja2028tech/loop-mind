"""LinkedIn Profile Extraction UPDATE SDD: real "Sign In with LinkedIn"
(OpenID Connect) — the only part of a LinkedIn integration LinkedIn's API
terms actually authorize. Returns exactly what the `openid profile email`
scopes provide: the member's name, email, and profile photo — nothing
else. LinkedIn's OpenID Connect flow never returns skills, projects,
certifications, education, or experience, so this module never attempts
to and never will; those fields keep coming from the existing best-effort
public-fetch + `linkedin_extraction_agent.py` path
(`registration_service.apply_linkedin_extraction`) unchanged, which this
module runs alongside, not instead of.

Gated entirely behind `settings.linkedin_client_id`/`linkedin_client_secret`
(a LinkedIn Developer app this project does not yet have real credentials
for) — `is_configured()` lets every caller report "not configured" honestly
rather than pretending extraction works with no real backing integration.
"""

from urllib.parse import urlencode

import requests

from backend.core.config import settings

_AUTHORIZE_URL = "https://www.linkedin.com/oauth/v2/authorization"
_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
_USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
_SCOPES = "openid profile email"
_REQUEST_TIMEOUT_SECONDS = 10


class LinkedInOAuthError(Exception):
    """Raised with a machine-readable `code` (§16's failure categories) —
    the caller must show a clear failure state, never a fabricated
    success, when this is raised."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


def is_configured() -> bool:
    return bool(settings.linkedin_client_id and settings.linkedin_client_secret)


def build_authorization_url(state: str) -> str:
    """Only meaningful when `is_configured()` is true — callers must check
    that first and report AUTHORIZATION_REQUIRED/not-configured otherwise,
    never build a URL pointing at a client_id that doesn't exist."""
    params = {
        "response_type": "code",
        "client_id": settings.linkedin_client_id,
        "redirect_uri": settings.linkedin_redirect_uri,
        "scope": _SCOPES,
        "state": state,
    }
    return f"{_AUTHORIZE_URL}?{urlencode(params)}"


def exchange_code_for_userinfo(code: str) -> dict:
    """Server-side authorization-code exchange (the client secret never
    reaches the frontend) followed by the OpenID Connect userinfo call.
    Returns LinkedIn's own userinfo payload
    (`sub`/`name`/`given_name`/`family_name`/`email`/`email_verified`/
    `picture`) verbatim — the caller maps only the fields that exist,
    never invents ones that don't."""
    if not is_configured():
        raise LinkedInOAuthError(
            "AUTHORIZATION_REQUIRED", "LinkedIn integration is not configured."
        )

    try:
        token_response = requests.post(
            _TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.linkedin_redirect_uri,
                "client_id": settings.linkedin_client_id,
                "client_secret": settings.linkedin_client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise LinkedInOAuthError("NETWORK_ERROR", str(exc)) from exc

    if token_response.status_code != 200:
        raise LinkedInOAuthError(
            "AUTHORIZATION_DENIED", f"Token exchange failed: {token_response.text[:300]}"
        )

    access_token = token_response.json().get("access_token")
    if not access_token:
        raise LinkedInOAuthError("API_ERROR", "LinkedIn did not return an access token.")

    try:
        userinfo_response = requests.get(
            _USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise LinkedInOAuthError("NETWORK_ERROR", str(exc)) from exc

    if userinfo_response.status_code != 200:
        raise LinkedInOAuthError(
            "API_ERROR", f"userinfo request failed: {userinfo_response.text[:300]}"
        )

    userinfo = userinfo_response.json()
    if not userinfo.get("name") and not userinfo.get("email"):
        raise LinkedInOAuthError(
            "NO_SUPPORTED_PROFILE_DATA", "LinkedIn returned no usable identity fields."
        )
    return userinfo


def download_profile_photo(picture_url: str) -> bytes:
    """Fetches the profile photo LinkedIn's own userinfo response pointed
    at (a trusted URL from LinkedIn's API, not user input) — capped so a
    misbehaving/huge response can't be used to abuse storage."""
    try:
        response = requests.get(picture_url, timeout=_REQUEST_TIMEOUT_SECONDS, stream=True)
    except requests.RequestException as exc:
        raise LinkedInOAuthError("NETWORK_ERROR", str(exc)) from exc
    if response.status_code != 200:
        raise LinkedInOAuthError("API_ERROR", "Could not download the LinkedIn profile photo.")
    content = response.content
    if len(content) > 8 * 1024 * 1024:
        raise LinkedInOAuthError("API_ERROR", "LinkedIn profile photo was unexpectedly large.")
    return content
