"""Recruiter Interview Invitation & Demo Email Specification §7-8: the
actual SMTP transport that delivers an interview invitation to a student's
inbox. Credentials come only from `backend.core.config.settings` (itself
sourced from environment/`.env`), never hardcoded in source. When the demo
mailbox isn't configured, `send_email` honestly reports that rather than
pretending to have sent anything — the same precedent as `linkedin_oauth_
service.py` reporting "not configured".
"""

import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from backend.core.config import settings


def is_configured() -> bool:
    return bool(
        settings.email_host
        and settings.email_username
        and settings.email_password
        and settings.email_from
    )


def send_email(*, to_address: str, subject: str, body: str) -> tuple[bool, str]:
    """Sends a real email via the configured SMTP transport. Returns
    (success, message) — `message` is a human-readable error on failure, or
    "sent" on success. Never raises: a transport failure (bad credentials,
    unreachable host, refused recipient) is reported back as a failed
    result so the caller can persist an honest FAILED status instead of
    crashing the approval workflow."""
    if not is_configured():
        return False, (
            "Email transport is not configured. Set EMAIL_HOST, EMAIL_USERNAME, "
            "EMAIL_PASSWORD, and EMAIL_FROM in the environment to enable actual sending."
        )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = (
        formataddr((settings.email_from_name, settings.email_from))
        if settings.email_from_name
        else settings.email_from
    )
    message["To"] = to_address
    message.set_content(body)

    try:
        with smtplib.SMTP(settings.email_host, settings.email_port, timeout=15) as server:
            server.starttls()
            server.login(settings.email_username, settings.email_password)
            server.send_message(message)
        return True, "sent"
    except (smtplib.SMTPException, OSError) as exc:
        return False, str(exc)
