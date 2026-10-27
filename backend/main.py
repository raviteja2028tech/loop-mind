"""LOOP-MIND FastAPI application entrypoint.

Run with:  uvicorn backend.main:app --reload --port 8011  (from repo root)

Phase 01 wired up the foundation (app, CORS, DB connectivity, health
check). Phase 03 added authentication (OTP + JWT) and role separation.
Phase 04 added the full master-data schema and the generated Company
Intelligence dataset. Phase 05 added Student Profile onboarding. Phase 06
adds the Student Intelligence multi-agent system (Skill Gap / Readiness /
Preparation Plan / What-If) and embeds Company Intelligence into Qdrant.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import backend.models  # noqa: F401  registers models on Base.metadata
from backend.core.config import settings
from backend.core.database import Base, SessionLocal, engine
from backend.core.seed import seed_demo_recruiter, seed_demo_student
from backend.core.seed_company_intelligence import seed_company_intelligence
from backend.core.seed_jobs import seed_jobs
from backend.routes import (
    auth,
    dashboard,
    health,
    intelligence,
    jobs,
    preparation_plan,
    profile,
    recruiter_analytics,
    recruiter_candidates,
    recruiter_dashboard,
    recruiter_interviews,
    recruiter_jobs,
    registration,
    skill_gap,
    students,
)
from backend.services.intelligence_service import ingest_company_intelligence_into_qdrant


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    if settings.environment != "production":
        with SessionLocal() as db:
            seed_demo_recruiter(db)
            seed_demo_student(db)
            seed_company_intelligence(db)
            seed_jobs(db)
            ingest_company_intelligence_into_qdrant(db)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(registration.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(intelligence.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(skill_gap.router, prefix="/api")
app.include_router(preparation_plan.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(recruiter_dashboard.router, prefix="/api")
app.include_router(recruiter_jobs.router, prefix="/api")
app.include_router(recruiter_candidates.router, prefix="/api")
app.include_router(recruiter_interviews.router, prefix="/api")
app.include_router(recruiter_analytics.router, prefix="/api")
