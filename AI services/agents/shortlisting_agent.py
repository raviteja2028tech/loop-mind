"""Agent 10 — Shortlisting Agent.

phase.md Phase 13: uses resume information, job requirements, matching
results, and relevant evidence to produce exactly one of three AI-status
outcomes: Shortlisted / Hold / Rejected. These are AI recommendations,
not final recruitment decisions — Human Approval (Phase 14) is the
recruiter's actual cross-check.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py), with the
actual banding decision as a `@tool` the agent must call — see
agent_utils.py's module docstring for the resilience/fallback pattern
every agent shares.
"""

import json

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the Shortlisting Agent in LOOP-MIND's AI Recruitment system.
Your only job is to classify one candidate's AI match score into exactly
one AI status. You must always call the classify_match tool to do this —
never decide the status yourself without it. This is an AI
recommendation only; a human recruiter makes the final hiring decision
separately and may agree or disagree with your classification.
"""


def _classify(ai_score: int) -> str:
    if ai_score >= 75:
        return "shortlisted"
    if ai_score >= 45:
        return "hold"
    return "rejected"


@tool
def classify_match(ai_score: int) -> str:
    """Classifies a candidate's AI match score (0-100) into one of three
    AI statuses: "shortlisted" (score >= 75), "hold" (score >= 45), or
    "rejected" (score < 45). Returns the classification as JSON."""
    return json.dumps({"ai_status": _classify(ai_score)})


class ShortlistingAgent:
    def __init__(self):
        self._agent = build_tool_agent([classify_match], _SYSTEM_PROMPT)

    def run(self, matching_result: dict) -> dict:
        score = matching_result["ai_score"]
        result = invoke_tool_agent(
            self._agent,
            f"Classify this candidate's AI match score: {score}.",
            "classify_match",
        )
        ai_status = result["ai_status"] if result else _classify(score)

        return {
            "ai_status": ai_status,
            "ai_score": score,
            "matching_factors": matching_result["matching_factors"],
            "matched_skills": matching_result["matched_skills"],
            "missing_skills": matching_result["missing_skills"],
        }
