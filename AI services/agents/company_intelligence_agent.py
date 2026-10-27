"""Agent 1 — Company Intelligence Agent.

spec.md phase.md Phase 06: analyzes company requirements, historical
requirements, current roles, recruitment patterns, successful-candidate
characteristics, historical recruitment outcomes.

Structured facts (required skills, experience/evidence/project
expectations) come from SQLite via the caller-supplied `company` dict —
spec.md §3: "Qdrant should not become the authoritative database." RAG
(rag.retrieve) supplies supporting narrative context (patterns,
successful-candidate profiles) that the Skill-Gap Agent later folds into
its reasoning text.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — the role
matching/shaping is a `@tool` so its output stays exact regardless of
whether a real model is configured; see agent_utils.py's module docstring
for the shared resilience/fallback pattern. The RAG retrieval itself needs
a live `QdrantClient`, which isn't JSON-tool-friendly, so it stays outside
the tool call and its (already-structured) result is passed in.
"""

import json

from langchain.tools import tool
from qdrant_client import QdrantClient
from rag.retrieve import search_company_knowledge

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the Company Intelligence Agent in LOOP-MIND's Student Intelligence
system. Given a company's role requirements, a target role, and retrieved
supporting context, your job is to call the analyze_company tool to match
the target role, shape the requirements, and attach the supporting
context. Always call the tool — never decide the match yourself.
"""


def _resolve_role(company: dict, target_role: str | None) -> tuple[dict | None, bool]:
    role_requirements = company.get("role_requirements", [])
    matched_role = None
    if target_role:
        matched_role = next(
            (
                r
                for r in role_requirements
                if r["role_title"].strip().lower() == target_role.strip().lower()
            ),
            None,
        )
    # No exact role match (or none requested): fall back to the
    # company's first defined role rather than returning nothing —
    # the student still gets a meaningful comparison target.
    role = matched_role or (role_requirements[0] if role_requirements else None)
    return role, matched_role is not None


def _analyze(company: dict, target_role: str | None, retrieved_context: list) -> dict:
    role, role_matched_exactly = _resolve_role(company, target_role)

    return {
        "company_id": company["company_id"],
        "company_name": company["company_name"],
        "target_role": role["role_title"] if role else target_role,
        "role_matched_exactly": role_matched_exactly,
        "required_skills": role["required_skills"] if role else [],
        "experience_expectation": role.get("experience_expectation") if role else None,
        "evidence_expectations": role.get("evidence_expectations", []) if role else [],
        "project_expectations": role.get("project_expectations", []) if role else [],
        "patterns": company.get("patterns", []),
        "successful_candidate_profiles": company.get("successful_candidate_profiles", []),
        "retrieved_context": retrieved_context,
    }


@tool
def analyze_company(company_json: str, target_role: str, retrieved_context_json: str) -> str:
    """Matches a target role against a company's defined roles (falling
    back to the company's first role if no exact match), shapes the
    role's requirements, and attaches already-retrieved supporting
    context. `company_json`/`retrieved_context_json` are JSON-encoded;
    `target_role` may be an empty string. Returns the full analysis as
    JSON."""
    company = json.loads(company_json)
    retrieved_context = json.loads(retrieved_context_json)
    return json.dumps(_analyze(company, target_role or None, retrieved_context))


class CompanyIntelligenceAgent:
    def __init__(self):
        self._agent = build_tool_agent([analyze_company], _SYSTEM_PROMPT)

    def run(
        self,
        client: QdrantClient,
        company: dict,
        target_role: str | None,
    ) -> dict:
        """`company` shape: {company_id, company_name, industry,
        role_requirements: [{role_title, required_skills:
        [{skill, min_proficiency}], experience_expectation,
        evidence_expectations, project_expectations}], patterns: [str],
        historical_requirements: [...], successful_candidate_profiles:
        [{role_title, profile_summary}]}."""
        role, _ = _resolve_role(company, target_role)
        query = f"{company['company_name']} {target_role or (role['role_title'] if role else '')}"
        try:
            retrieved_context = search_company_knowledge(
                client, query, company_id=company["company_id"], top_k=5
            )
        except Exception:
            # RAG is supporting context, not the source of truth — a
            # retrieval failure must not break the structured analysis.
            retrieved_context = []

        result = invoke_tool_agent(
            self._agent,
            (
                f"Analyze this company's requirements for the target role. "
                f"Company: {json.dumps(company)}. Target role: {target_role or ''}. "
                f"Retrieved context: {json.dumps(retrieved_context)}."
            ),
            "analyze_company",
        )
        return result if result else _analyze(company, target_role, retrieved_context)
