"""Multi-Agent System 1 — Student Intelligence.

phase.md Phase 06:

    Company Intelligence Agent
              |
    Student Skill Analysis Agent
              |
    Placement Readiness Agent
              |
    Skill-Gap Analysis Agent
              |
    Preparation Plan Agent
              |
    What-If Analysis Agent

Composed as a genuine LangChain `RunnableSequence` (via `RunnableLambda`
and the `|` operator) over a shared state dict, so this is real LangChain
orchestration rather than five function calls dressed up as one. What-If
is invoked separately from the other five, matching spec.md's own
description of it as a student-triggered, on-demand analysis rather than
a pipeline stage that always runs.

Standalone (no `backend` dependency) — see rag/vector_store.py's
module docstring for why and how this gets imported.
"""

from agents.company_intelligence_agent import CompanyIntelligenceAgent
from agents.placement_readiness_agent import PlacementReadinessAgent
from agents.preparation_plan_agent import PreparationPlanAgent
from agents.skill_gap_analysis_agent import SkillGapAnalysisAgent
from agents.student_skill_analysis_agent import StudentSkillAnalysisAgent
from agents.what_if_analysis_agent import WhatIfAnalysisAgent
from langchain_core.runnables import RunnableLambda
from qdrant_client import QdrantClient


def _build_pipeline(qdrant: QdrantClient):
    company_agent = CompanyIntelligenceAgent()
    skill_agent = StudentSkillAnalysisAgent()
    readiness_agent = PlacementReadinessAgent()
    gap_agent = SkillGapAnalysisAgent()
    plan_agent = PreparationPlanAgent()

    step_company_intel = RunnableLambda(
        lambda state: {
            **state,
            "company_intel": company_agent.run(qdrant, state["company"], state["target_role"]),
        }
    )
    step_student_analysis = RunnableLambda(
        lambda state: {**state, "student_analysis": skill_agent.run(state["student"])}
    )
    step_readiness = RunnableLambda(
        lambda state: {
            **state,
            "readiness": readiness_agent.run(state["company_intel"], state["student_analysis"]),
        }
    )
    step_skill_gap = RunnableLambda(
        lambda state: {
            **state,
            "skill_gap": gap_agent.run(
                state["company_intel"], state["student_analysis"], state["readiness"]
            ),
        }
    )
    step_preparation_plan = RunnableLambda(
        lambda state: {
            **state,
            "preparation_plan": plan_agent.run(
                state["skill_gap"], (state["student"].get("academic") or {}).get("current_year")
            ),
        }
    )

    return (
        step_company_intel
        | step_student_analysis
        | step_readiness
        | step_skill_gap
        | step_preparation_plan
    )


def run_student_intelligence_pipeline(
    qdrant: QdrantClient,
    *,
    company: dict,
    student: dict,
    target_role: str | None,
) -> dict:
    """Runs Agents 1-5 in sequence. Returns the accumulated state dict
    containing `company_intel`, `student_analysis`, `readiness`,
    `skill_gap`, and `preparation_plan`."""
    pipeline = _build_pipeline(qdrant)
    return pipeline.invoke({"company": company, "student": student, "target_role": target_role})


def run_what_if(
    qdrant: QdrantClient,
    *,
    company: dict,
    student: dict,
    target_role: str | None,
    question: str,
) -> dict:
    """Agent 6, run on demand against the same context the main pipeline
    would compute (spec.md: uses "current student state" + "company
    requirements" + "current skill-gap context"). Also passes the
    company's full `role_requirements` (every role, not just the selected
    one) through unchanged, so the agent can report which other roles at
    this company value the asked-about skill — Student Portal UPDATE SDD
    §18's "relevant roles" information, from real stored data."""
    context = run_student_intelligence_pipeline(
        qdrant, company=company, student=student, target_role=target_role
    )
    what_if_agent = WhatIfAnalysisAgent()
    return what_if_agent.run(
        question,
        context["company_intel"],
        context["student_analysis"],
        context["readiness"],
        context["skill_gap"],
        company.get("role_requirements", []),
    )
