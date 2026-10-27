"""Email Invitation & Session Persistence Fix Specification §1.1/§3: the
sender identity (From address/name) is configured independently of any
student's email and must never depend on it."""

from unittest.mock import patch

from backend.core.config import settings
from backend.services import email_service


def test_send_email_reports_not_configured_without_credentials():
    with (
        patch.object(settings, "email_host", ""),
        patch.object(settings, "email_username", ""),
        patch.object(settings, "email_password", ""),
        patch.object(settings, "email_from", ""),
    ):
        sent, message = email_service.send_email(
            to_address="student@example.com", subject="Subject", body="Body"
        )
    assert sent is False
    assert "not configured" in message.lower()


def test_send_email_uses_configured_sender_name_and_address():
    with (
        patch.object(settings, "email_host", "smtp.example.com"),
        patch.object(settings, "email_username", "demo@example.com"),
        patch.object(settings, "email_password", "app-password"),
        patch.object(settings, "email_from", "demo@example.com"),
        patch.object(settings, "email_from_name", "LOOP-MIND Recruiting"),
        patch("backend.services.email_service.smtplib.SMTP") as mock_smtp,
    ):
        mock_server = mock_smtp.return_value.__enter__.return_value
        sent, message = email_service.send_email(
            to_address="student@example.com", subject="Subject", body="Body"
        )

    assert sent is True
    assert message == "sent"
    sent_message = mock_server.send_message.call_args[0][0]
    assert sent_message["From"] == "LOOP-MIND Recruiting <demo@example.com>"
    assert sent_message["To"] == "student@example.com"
    # The sender identity never depends on, or is derived from, the
    # recipient's own address.
    assert "student@example.com" not in sent_message["From"]
