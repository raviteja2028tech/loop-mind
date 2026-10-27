"""Agent 6 — What-If Analysis Agent.

phase.md Phase 06 + spec.md "Try What-If Analysis": answers questions
like "What if I learn Generative AI?" or "What should I improve first to
become ready for Company X?" using the student's current state and
company requirements — not a fixed canned answer.

Student Portal UPDATE SDD §16-19: the result must include a genuinely
calculated projected-readiness percentage (current vs hypothetical) and
relevant-roles/demand information — both computed from real stored data,
never fabricated:

* The projection reuses `placement_readiness_agent._calculate` (the same
  agent, not a duplicate) against a *copy* of the student's skills with
  the asked-about topic hypothetically raised to the target role's
  required proficiency — the student's real stored skills are never
  touched, matching §17's "must not automatically modify the student's
  real profile."
* "Relevant roles" comes from the target company's own other role
  requirements (already fetched as part of Company Intelligence's input,
  passed straight through here) — real data already in the database, not
  an invented demand dataset.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — the topic
extraction and relevance analysis is a `@tool` so the answer stays exact
regardless of whether a real model is configured; see agent_utils.py's
module docstring for the shared resilience/fallback pattern.
"""

import json
import re

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent
from agents.placement_readiness_agent import PROFICIENCY_RANK
from agents.placement_readiness_agent import _calculate as _calculate_readiness

# General topics a student might ask about beyond the target's exact
# required-skill list, so "What if I learn Generative AI?" resolves to a
# topic even when it isn't one of the company's listed requirements.
_KNOWN_TOPICS = [
    "generative ai",
    "machine learning",
    "deep learning",
    "data structures & algorithms",
    "dsa",
    "system design",
    "cloud",
    "aws",
    "gcp",
    "sql",
    "python",
    "java",
    "javascript",
    "react",
    "node.js",
    "kubernetes",
    "docker",
    "networking",
    "security",
]

_SYSTEM_PROMPT = """
You are the What-If Analysis Agent in LOOP-MIND's Student Intelligence
system. A student asks a hypothetical question like "What if I learn
Generative AI?" — your job is to call the answer_what_if tool with the
question, the target company's requirements, the student's current
skills, their current readiness, their skill gap, and the company's
other role requirements, so it can identify the topic, calculate a
genuine projected readiness percentage, find relevant roles, and produce
a grounded answer. Always call the tool — never answer from general
knowledge alone, and never invent a percentage or role.
"""


def _extract_topic(question: str, required_skills: list[dict]) -> str | None:
    question_lower = question.lower()
    # Prefer an exact required-skill match (most specific/actionable).
    for requirement in required_skills:
        if requirement["skill"].lower() in question_lower:
            return requirement["skill"]
    for topic in sorted(_KNOWN_TOPICS, key=len, reverse=True):
        if topic in question_lower:
            return topic
    # Fall back to the longest capitalized phrase in the question, if any.
    capitalized = re.findall(r"\b[A-Z][a-zA-Z0-9+.#]*(?:\s+[A-Z][a-zA-Z0-9+.#]*)*\b", question)
    return max(capitalized, key=len) if capitalized else None


def _project_readiness(topic: str, company_intel: dict, student_analysis: dict) -> int | None:
    """Simulates the topic being learned to the target role's required
    level (or, if the topic isn't one of this role's requirements, an
    Advanced level that simply won't move a role-requirement-based score)
    and reruns the real Placement Readiness calculation — never a
    fabricated number. Operates on a *copy* of the skill list only."""
    required_skills = company_intel.get("required_skills", [])
    requirement = next(
        (r for r in required_skills if r["skill"].strip().lower() == topic.strip().lower()), None
    )
    target_level = requirement.get("min_proficiency", "Advanced") if requirement else "Advanced"

    skills = [dict(s) for s in student_analysis.get("skills", [])]
    topic_key = topic.strip().lower()
    match = next((s for s in skills if s["skill_name"].strip().lower() == topic_key), None)
    if match is None:
        skills.append({"skill_name": topic, "proficiency": target_level})
    elif PROFICIENCY_RANK.get(match.get("proficiency"), 0) < PROFICIENCY_RANK.get(target_level, 1):
        match["proficiency"] = target_level

    projected = _calculate_readiness(company_intel, {**student_analysis, "skills": skills})
    return projected["readiness_percentage"]


def _relevant_roles(topic: str, all_role_requirements: list[dict]) -> list[str]:
    return [
        role["role_title"]
        for role in all_role_requirements
        if any(
            s.get("skill", "").strip().lower() == topic.strip().lower()
            for s in role.get("required_skills", [])
        )
    ]


def _analyze(
    question: str,
    company_intel: dict,
    student_analysis: dict,
    readiness: dict,
    skill_gap: dict,
    all_role_requirements: list[dict],
) -> dict:
    required_skills = company_intel.get("required_skills", [])
    topic = _extract_topic(question, required_skills)

    is_required = bool(topic and any(r["skill"].lower() == topic.lower() for r in required_skills))
    is_top_priority = bool(
        topic
        and skill_gap.get("priority_areas")
        and skill_gap["priority_areas"][0]["skill"].lower() == topic.lower()
    )

    current_pct = readiness.get("readiness_percentage")
    projected_pct = _project_readiness(topic, company_intel, student_analysis) if topic else None
    relevant_roles = _relevant_roles(topic, all_role_requirements) if topic else []

    if topic is None:
        topic_clause = "I couldn't identify a specific skill or topic in that question. "
        relevance_clause = 'Try naming a specific skill, e.g. "What if I learn System Design?"'
        priority_clause = ""
        projection_clause = ""
    else:
        topic_clause = f"Regarding {topic}: "
        if is_required:
            relevance_clause = (
                f"this is one of the skills {company_intel['company_name']} looks for "
                f"for {company_intel.get('target_role') or 'this role'}, so improving it "
                f"directly increases your readiness. "
            )
        else:
            relevance_clause = (
                f"this is not currently listed among {company_intel['company_name']}'s "
                f"requirements for {company_intel.get('target_role') or 'this role'}, so it "
                f"would broaden your profile without directly moving your readiness score. "
            )
        priority_clause = "It is currently your top priority gap. " if is_top_priority else ""

        if current_pct is not None and projected_pct is not None:
            if projected_pct > current_pct:
                projection_clause = (
                    f"Learning {topic} to the level {company_intel['company_name']} expects would "
                    f"move your readiness from {current_pct}% to {projected_pct}%."
                )
            else:
                projection_clause = (
                    f"Your readiness would remain at {projected_pct}% — you already meet or "
                    f"exceed the expected level for {topic} here."
                )
        else:
            projection_clause = ""

    answer = f"{topic_clause}{relevance_clause}{priority_clause}{projection_clause}"

    return {
        "question": question,
        "topic": topic,
        "relevant_to_target": is_required,
        "is_top_priority": is_top_priority,
        "answer": answer,
        "current_readiness_percentage": current_pct,
        "projected_readiness_percentage": projected_pct,
        "relevant_roles": relevant_roles,
    }


@tool
def answer_what_if(
    question: str,
    company_intel_json: str,
    student_analysis_json: str,
    readiness_json: str,
    skill_gap_json: str,
    all_role_requirements_json: str,
) -> str:
    """Identifies the skill/topic a student's what-if question is about,
    determines whether it's relevant to their target company/role,
    calculates the genuine projected readiness percentage if they reached
    the required level for it, finds other roles at the company requiring
    it, and writes a grounded answer. All `*_json` arguments are
    JSON-encoded. Returns the full answer as JSON."""
    company_intel = json.loads(company_intel_json)
    student_analysis = json.loads(student_analysis_json)
    readiness = json.loads(readiness_json)
    skill_gap = json.loads(skill_gap_json)
    all_role_requirements = json.loads(all_role_requirements_json)
    return json.dumps(
        _analyze(
            question, company_intel, student_analysis, readiness, skill_gap, all_role_requirements
        )
    )


class WhatIfAnalysisAgent:
    def __init__(self):
        self._agent = build_tool_agent([answer_what_if], _SYSTEM_PROMPT)

    def run(
        self,
        question: str,
        company_intel: dict,
        student_analysis: dict,
        readiness: dict,
        skill_gap: dict,
        all_role_requirements: list[dict],
    ) -> dict:
        result = invoke_tool_agent(
            self._agent,
            (
                f"Answer this what-if question: {question!r}. "
                f"Company intel: {json.dumps(company_intel)}. "
                f"Student analysis: {json.dumps(student_analysis)}. "
                f"Readiness: {json.dumps(readiness)}. "
                f"Skill gap: {json.dumps(skill_gap)}. "
                f"Other role requirements at this company: {json.dumps(all_role_requirements)}."
            ),
            "answer_what_if",
        )
        return (
            result
            if result
            else _analyze(
                question,
                company_intel,
                student_analysis,
                readiness,
                skill_gap,
                all_role_requirements,
            )
        )
