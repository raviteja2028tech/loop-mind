"""Agent 3 — Placement Readiness Agent.

phase.md Phase 06: compares Student Profile + Company Intelligence +
Target Job -> Placement Readiness. spec.md Skill Gap page: the readiness
percentage and status message must be calculated, never hardcoded.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — the
calculation itself is a `@tool` so its output stays exact regardless of
whether a real model is configured; see agent_utils.py's module docstring
for the shared resilience/fallback pattern.
"""

import json

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

PROFICIENCY_RANK = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

_SYSTEM_PROMPT = """
You are the Placement Readiness Agent in LOOP-MIND's Student Intelligence
system. Given a target company's required skills and a student's actual
skills, your job is to call the calculate_readiness tool to compute the
readiness percentage and status message. Always call the tool — never
compute the score yourself.
"""


def _calculate(company_intel: dict, student_analysis: dict) -> dict:
    required_skills = company_intel.get("required_skills", [])
    student_skills_by_name = {
        s["skill_name"].strip().lower(): s for s in student_analysis.get("skills", [])
    }

    if not required_skills:
        return {
            "readiness_percentage": 0,
            "status_message": "Set a target company and role to see your readiness.",
            "matched_skills": [],
            "partially_matched_skills": [],
            "unmatched_skills": [],
        }

    matched, partial, unmatched = [], [], []
    score = 0.0
    for requirement in required_skills:
        name = requirement["skill"]
        required_rank = PROFICIENCY_RANK.get(requirement.get("min_proficiency", "Beginner"), 1)
        student_skill = student_skills_by_name.get(name.strip().lower())
        if student_skill is None:
            unmatched.append(name)
            continue
        student_rank = PROFICIENCY_RANK.get(student_skill["proficiency"], 0)
        if student_rank >= required_rank:
            matched.append(name)
            score += 1.0
        else:
            partial.append(name)
            score += 0.5

    readiness_percentage = round((score / len(required_skills)) * 100)

    if readiness_percentage >= 75:
        status_message = "You are on track!"
    elif readiness_percentage >= 40:
        status_message = "Making progress — a few key gaps remain."
    else:
        status_message = "Significant preparation needed for this target."

    return {
        "readiness_percentage": readiness_percentage,
        "status_message": status_message,
        "matched_skills": matched,
        "partially_matched_skills": partial,
        "unmatched_skills": unmatched,
    }


@tool
def calculate_readiness(company_intel_json: str, student_analysis_json: str) -> str:
    """Compares a target role's required skills against a student's
    actual skills and computes the readiness percentage, status message,
    and matched/partially-matched/unmatched skill lists. Inputs are
    JSON-encoded dicts. Returns the full result as JSON."""
    company_intel = json.loads(company_intel_json)
    student_analysis = json.loads(student_analysis_json)
    return json.dumps(_calculate(company_intel, student_analysis))


class PlacementReadinessAgent:
    def __init__(self):
        self._agent = build_tool_agent([calculate_readiness], _SYSTEM_PROMPT)

    def run(self, company_intel: dict, student_analysis: dict) -> dict:
        result = invoke_tool_agent(
            self._agent,
            (
                "Calculate this student's placement readiness against the target role. "
                f"Company intel: {json.dumps(company_intel)}. "
                f"Student analysis: {json.dumps(student_analysis)}."
            ),
            "calculate_readiness",
        )
        return result if result else _calculate(company_intel, student_analysis)
