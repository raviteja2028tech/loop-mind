"""Shared test fixtures.

Each test function gets its own fresh in-memory SQLite database via the
`client` fixture, rather than modules sharing (and silently clobbering)
a single `app.dependency_overrides` entry — that bug previously made
whichever test module was imported last "win" for the entire session.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.config import settings
from backend.core.database import Base, get_db
from backend.core.seed import seed_demo_recruiter, seed_demo_student
from backend.main import app


@pytest.fixture(autouse=True)
def _no_real_email_transport(monkeypatch):
    """The test suite must never depend on, or be broken by, whatever real
    SMTP credentials a developer's own local `.env` happens to contain —
    and must never make a real network call to an actual mail provider
    just by running `pytest`. Every test starts with email transport
    forced "not configured"; a test that specifically wants to exercise a
    real send explicitly re-patches these fields itself (and mocks
    `smtplib.SMTP`), overriding this default only for its own duration."""
    monkeypatch.setattr(settings, "email_host", "")
    monkeypatch.setattr(settings, "email_username", "")
    monkeypatch.setattr(settings, "email_password", "")
    monkeypatch.setattr(settings, "email_from", "")
    monkeypatch.setattr(settings, "email_from_name", "")


def complete_registration(client, mobile: str, draft_token: str) -> str:
    """Student Create Account UPDATE SDD: no test may assume a real
    student account exists straight after OTP verification — `verify-otp`
    now only returns a registration-draft token. This carries that draft
    through the minimum required Basic Information + consent to Create
    Account, returning the resulting real student JWT, so every other
    test's `_register`/`_register_student` helper can keep returning a
    working student token exactly as before."""
    headers = {"Authorization": f"Bearer {draft_token}"}
    client.put(
        "/api/registration/draft/basic-info",
        json={
            "full_name": "Test Student",
            "date_of_birth": "2002-01-01",
            "gender": "male",
            "email": f"{mobile}@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Bengaluru",
        },
        headers=headers,
    )
    client.put(
        "/api/registration/draft/consent",
        json={
            "consent_use_information": True,
            "consent_learning_experience": True,
            "consent_anonymized_intelligence": True,
        },
        headers=headers,
    )
    res = client.post("/api/registration/create-account", headers=headers)
    return res.json()["token"]


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with testing_session_local() as db:
        seed_demo_recruiter(db)
        seed_demo_student(db)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)
