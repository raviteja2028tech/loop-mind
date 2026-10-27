"""Agent 5 — Preparation Plan Agent.

phase.md Phase 06 + spec.md §2.4 "Year-Aware Preparation Plan":
individualized short/medium/long-term plans that update when skills,
progress, or target company change. Versioning itself (marking the
previous plan historical, assigning the next version number) is a
persistence concern owned by backend/services/intelligence_service.py —
this agent only produces the plan content for a given input state.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — plan
construction is a `@tool` so its output stays exact regardless of
whether a real model is configured; see agent_utils.py's module docstring
for the shared resilience/fallback pattern.
"""

import json

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the Preparation Plan Agent in LOOP-MIND's Student Intelligence
system. Given a student's skill gap and current year, your job is to call
the build_plan tool to produce a year-aware, priority-ordered preparation
plan. Always call the tool — never write the plan yourself.
"""

_YEAR_EMPHASIS = {
    "1st Year": (
        "long-term",
        "Focus on fundamentals, broad learning, and building initial evidence.",
    ),
    "2nd Year": ("medium-term", "Deepen skills and ship more substantial projects."),
    "3rd Year": (
        "short-term",
        "Prioritize company-focused skills, DSA, and interview preparation.",
    ),
    "Final Year": ("short-term", "Focus tightly on placement-ready, company-specific preparation."),
}


def _build(skill_gap: dict, current_year: str | None) -> dict:
    horizon, year_guidance = _YEAR_EMPHASIS.get(
        current_year,
        ("medium-term", "Balance building new skills with deepening existing ones."),
    )

    items = []
    for area in skill_gap.get("priority_areas", []):
        if area["priority"] == "Low":
            action = f"Attach a project or certification link as evidence for {area['skill']}."
            category = "Evidence"
        elif area["priority"] == "High":
            action = f"Learn {area['skill']} from the ground up and build a small project using it."
            category = "Missing Skill"
        else:
            action = (
                f"Strengthen {area['skill']} toward the level "
                f"{skill_gap['target_company']} expects."
            )
            category = "Skill Depth"

        items.append(
            {
                "skill": area["skill"],
                "category": category,
                "priority": area["priority"],
                "horizon": horizon if area["priority"] == "High" else "medium-term",
                "action": action,
            }
        )

    return {
        "target_company": skill_gap.get("target_company"),
        "target_role": skill_gap.get("target_role"),
        "horizon_summary": horizon,
        "year_guidance": year_guidance,
        "items": items,
    }


@tool
def build_plan(skill_gap_json: str, current_year: str) -> str:
    """Builds a year-aware, priority-ordered preparation plan from a
    student's skill gap. `skill_gap_json` is a JSON-encoded dict;
    `current_year` may be an empty string. Returns the full plan as
    JSON."""
    skill_gap = json.loads(skill_gap_json)
    return json.dumps(_build(skill_gap, current_year or None))


class PreparationPlanAgent:
    def __init__(self):
        self._agent = build_tool_agent([build_plan], _SYSTEM_PROMPT)

    def run(self, skill_gap: dict, current_year: str | None) -> dict:
        result = invoke_tool_agent(
            self._agent,
            (
                f"Build a preparation plan for this student's skill gap: "
                f"{json.dumps(skill_gap)}. Current year: {current_year or ''}."
            ),
            "build_plan",
        )
        return result if result else _build(skill_gap, current_year)
