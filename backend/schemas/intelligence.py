from datetime import datetime

from pydantic import BaseModel


class TargetContext(BaseModel):
    company_name: str
    target_role: str | None = None


class SkillGapAnalysisOut(BaseModel):
    id: int
    target_company: str | None
    target_role: str | None
    analysis: dict
    created_at: datetime


class PreparationPlanOut(BaseModel):
    id: int
    target_company: str | None
    target_role: str | None
    version: int
    status: str
    plan: dict
    created_at: datetime


class WhatIfRequest(TargetContext):
    question: str


class WhatIfResultOut(BaseModel):
    id: int
    question: str
    result: dict
    created_at: datetime
