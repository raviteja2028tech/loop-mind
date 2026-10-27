"""Preparation Plan page — phase.md Phase 09. Shapes the stored current
PreparationPlan (backend/services/intelligence_service.py, Phase 06) plus
Year-Wise Focus / Goals / AI Recommendations into the exact reference
layout structure.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel


class GenerateIn(BaseModel):
    company_name: str
    target_role: str | None = None
    academic_year: str | None = None


class GoalIn(BaseModel):
    kind: Literal["short_term", "long_term"]
    text: str


class GoalOut(BaseModel):
    id: str
    text: str
    completed: bool


class YearFocusOut(BaseModel):
    year: str
    focus_text: str
    is_current: bool


class RecommendationOut(BaseModel):
    title: str


class PlanRowOut(BaseModel):
    skill: str
    category: str
    filter_category: str
    current_level: str
    target_level: str
    start_date: date
    end_date: date
    status: str
    priority: str
    resources: str


class ReadinessSummaryOut(BaseModel):
    has_analysis: bool
    readiness_percentage: int | None = None
    status_message: str | None = None


class PreparationPlanPageOut(BaseModel):
    target_company: str | None
    target_role: str | None
    academic_year: str | None
    company_options: list[str]
    role_options: list[str]
    academic_year_options: list[str]
    readiness: ReadinessSummaryOut
    year_wise_focus: list[YearFocusOut]
    short_term_goals: list[GoalOut]
    long_term_goals: list[GoalOut]
    recommendations: list[RecommendationOut]
    has_plan: bool
    plan_version: int | None = None
    plan_status: str | None = None
    plan_items: list[PlanRowOut]
