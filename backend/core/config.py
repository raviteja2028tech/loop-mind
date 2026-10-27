"""Application settings.

spec.md — Backend stack: Python, FastAPI, Pydantic, SQLAlchemy, JWT, OTP.
SQLite is the primary database (§ "FINAL BUILD TECHNOLOGY & AI SPECIFICATION" §4).
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "LOOP-MIND API"
    environment: str = "development"

    database_url: str = (
        f"sqlite:///{(REPO_ROOT / 'databases' / 'sqlite' / 'loop_mind.db').as_posix()}"
    )

    jwt_secret_key: str = "dev-secret-change-me-in-production-please-32b"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24

    # LinkedIn Profile Extraction UPDATE SDD: real "Sign In with LinkedIn"
    # (OpenID Connect) support for name/email/profile-photo — genuinely
    # authorized, never a scrape. Empty by default (no LinkedIn Developer
    # app exists for this project yet); `linkedin_oauth_service.py`
    # reports "not configured" honestly rather than pretending to work
    # until real values are set via a `.env` file or real env vars.
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    linkedin_redirect_uri: str = "http://localhost:5180/linkedin/oauth-callback"

    # Recruiter Interview Invitation & Demo Email Specification §7: a real
    # SMTP transport for sending interview invitations, configured only
    # through environment/`.env` — never hardcoded into source. Empty by
    # default (no demo mailbox exists for this project yet); `email_service`
    # reports "not configured" honestly rather than pretending to send
    # until real values are set, the same precedent as `linkedin_client_id`
    # above.
    email_provider: str = "smtp"
    email_host: str = ""
    email_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_from: str = ""
    # Email Invitation & Session Persistence Fix Specification §1.1/§3: a
    # display name for the recruiter/demo sender ("LOOP-MIND Recruiting"),
    # never the student's own name or email — the sender identity is
    # entirely independent of who the invitation is addressed to.
    email_from_name: str = ""

    # Native React Native requests aren't subject to browser CORS at all —
    # these extra origins only matter when the mobile app runs via
    # `expo start --web` (phase.md Phase 19), which does run in a browser.
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5180",
        "http://localhost:8081",
        "http://localhost:19006",
        # LAN access (same-wifi demo) — the frontend dev server is reachable
        # at this machine's local IP so devices on the same network can open
        # it; requests still proxy server-side to the backend (see
        # frontend/vite.config.ts), but this covers any direct call too.
        "http://172.16.128.80:5180",
    ]


settings = Settings()

# spec.md "FILE & STORAGE ARCHITECTURE": storage/ holds resumes, documents,
# uploaded files and datasets. Profile photos aren't a separately named
# subdirectory in the spec, so they live under documents/ rather than
# inventing a new top-level storage folder.
STORAGE_ROOT = REPO_ROOT / "storage"
PROFILE_PHOTOS_DIR = STORAGE_ROOT / "documents" / "profile_photos"
RESUMES_DIR = STORAGE_ROOT / "documents" / "resumes"
CERTIFICATES_DIR = STORAGE_ROOT / "documents" / "certificates"
