"""Agent 4 — Skill-Gap Analysis Agent.

phase.md Phase 06: identifies missing skills, weak skills, missing
evidence, requirement mismatches, readiness gaps, priority gaps, reasons
behind the assessment. spec.md Skill Gap page §14: "Already Strong /
Needs Improvement / Missing / Not Relevant" distribution categories.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — the
classification itself is a `@tool` so its output stays exact regardless
of whether a real model is configured; see agent_utils.py's module
docstring for the shared resilience/fallback pattern.
"""

import json

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent
from agents.placement_readiness_agent import PROFICIENCY_RANK

_SYSTEM_PROMPT = """
You are the Skill-Gap Analysis Agent in LOOP-MIND's Student Intelligence
system. Given a target company's required skills, a student's actual
skills, and their placement readiness, your job is to call the
analyze_skill_gap tool to classify every required skill into Already
Strong, Needs Improvement, or Missing, identify skills lacking
supporting evidence, rank priority areas, and produce the reasoning
behind the assessment. Always call the tool — never classify skills
yourself.
"""


def _classify(company_intel: dict, student_analysis: dict, readiness: dict) -> dict:
    required_skills = company_intel.get("required_skills", [])
    student_skills_by_name = {
        s["skill_name"].strip().lower(): s for s in student_analysis.get("skills", [])
    }
    skills_without_evidence = set(student_analysis.get("skills_without_evidence", []))

    existing_skills: list[str] = []
    weak_skills: list[str] = []
    missing_skills: list[str] = []
    missing_evidence: list[str] = []
    priority_areas: list[dict] = []

    for requirement in required_skills:
        name = requirement["skill"]
        required_rank = PROFICIENCY_RANK.get(requirement.get("min_proficiency", "Beginner"), 1)
        student_skill = student_skills_by_name.get(name.strip().lower())

        if student_skill is None:
            missing_skills.append(name)
            priority_areas.append(
                {
                    "skill": name,
                    "priority": "High",
                    "reason": "Required skill not yet present in the student's profile.",
                }
            )
            continue

        student_rank = PROFICIENCY_RANK.get(student_skill["proficiency"], 0)
        if student_rank < required_rank:
            weak_skills.append(name)
            priority_areas.append(
                {
                    "skill": name,
                    "priority": "Medium",
                    "reason": (
                        f"Current level ({student_skill['proficiency']}) is below the "
                        f"required level ({requirement.get('min_proficiency', 'Beginner')})."
                    ),
                }
            )
        else:
            existing_skills.append(name)
            if name in skills_without_evidence:
                missing_evidence.append(name)
                priority_areas.append(
                    {
                        "skill": name,
                        "priority": "Low",
                        "reason": (
                            "Skill is claimed at a sufficient level but has no supporting evidence."
                        ),
                    }
                )

    # Not Relevant: skills the student has that this target simply
    # doesn't ask for — spec.md §14's fourth distribution category.
    required_names = {r["skill"].strip().lower() for r in required_skills}
    not_relevant = [
        s["skill_name"]
        for s in student_analysis.get("skills", [])
        if s["skill_name"].strip().lower() not in required_names
    ]

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    priority_areas.sort(key=lambda a: priority_order.get(a["priority"], 3))

    missing_clause = (
        f"Missing required skills: {', '.join(missing_skills)}. " if missing_skills else ""
    )
    weak_clause = (
        f"Skills below the required level: {', '.join(weak_skills)}. " if weak_skills else ""
    )
    strength_clause = f"Already strong in: {', '.join(existing_skills)}." if existing_skills else ""
    reasoning = (
        f"{company_intel['company_name']} is assessed as "
        f"{readiness['readiness_percentage']}% ready for "
        f"{company_intel.get('target_role') or 'the selected role'}. "
        f"{missing_clause}{weak_clause}{strength_clause or 'No strong matches identified yet.'}"
    )

    return {
        "target_company": company_intel["company_name"],
        "target_role": company_intel.get("target_role"),
        "readiness_percentage": readiness["readiness_percentage"],
        "existing_skills": existing_skills,
        "weak_skills": weak_skills,
        "missing_skills": missing_skills,
        "missing_evidence": missing_evidence,
        "not_relevant_skills": not_relevant,
        "priority_areas": priority_areas,
        "reasoning": reasoning,
    }


@tool
def analyze_skill_gap(
    company_intel_json: str, student_analysis_json: str, readiness_json: str
) -> str:
    """Classifies a target role's required skills against a student's
    actual skills into Already Strong / Needs Improvement / Missing /
    Not Relevant, flags skills without supporting evidence, ranks
    priority areas, and writes the reasoning behind the assessment.
    Inputs are JSON-encoded dicts; returns the full analysis as JSON."""
    company_intel = json.loads(company_intel_json)
    student_analysis = json.loads(student_analysis_json)
    readiness = json.loads(readiness_json)
    return json.dumps(_classify(company_intel, student_analysis, readiness))


class SkillGapAnalysisAgent:
    def __init__(self):
        self._agent = build_tool_agent([analyze_skill_gap], _SYSTEM_PROMPT)

    def run(self, company_intel: dict, student_analysis: dict, readiness: dict) -> dict:
        result = invoke_tool_agent(
            self._agent,
            (
                "Analyze this student's skill gap against the target role. "
                f"Company intel: {json.dumps(company_intel)}. "
                f"Student analysis: {json.dumps(student_analysis)}. "
                f"Readiness: {json.dumps(readiness)}."
            ),
            "analyze_skill_gap",
        )
        return result if result else _classify(company_intel, student_analysis, readiness)
