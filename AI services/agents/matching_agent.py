"""Agent 9 — Matching Agent.

phase.md Phase 13: "Compares Candidate Profile VS Job Requirements and
determines alignment."

The AI Score blends two genuine signals:
- a deterministic skill-coverage score (does the candidate have each of
  the job's required skills, at all — the job model stores a flat skill
  list with no per-skill proficiency requirement, unlike Company
  Intelligence's role requirements, so presence is the honest comparison
  available here);
- a semantic-similarity score computed against the candidate's own stored
  embedding (Agent 8) via real cosine similarity — not a fabricated
  percentage.

Also stores the job's own requirement text into Qdrant's
`job_requirements` collection (provisioned since Phase 04, used for the
first time here).

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — the
skill-coverage comparison and final scoring/classification is a `@tool`
so it stays exact regardless of whether a real model is configured (see
agent_utils.py's module docstring for the shared resilience/fallback
pattern); the embedding vectors and Qdrant upsert need a live
`QdrantClient` and aren't JSON-tool-friendly, so they stay outside the
tool call, and their (already-computed) semantic-similarity percentage is
passed in.
"""

import json
import math
import uuid

from embeddings.model import embed_text
from langchain.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from rag.vector_store import COLLECTION_JOB_REQUIREMENTS

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_NAMESPACE = uuid.UUID("6f6f6c6d-696e-6400-0000-00000000cafe")

_SYSTEM_PROMPT = """
You are the Matching Agent in LOOP-MIND's AI Recruitment system. Given a
job's required skills, a candidate's skills, and their already-computed
semantic similarity, your job is to call the score_match tool to compute
skill coverage, the blended AI score, and the matching-factors label.
Always call the tool — never score the match yourself.
"""


def _point_id(job_id: int) -> str:
    return str(uuid.uuid5(_NAMESPACE, f"job-requirements|{job_id}"))


def _job_text(job: dict) -> str:
    skills = ", ".join(job.get("required_skills", [])) or "no specific skills listed"
    return (
        f"{job['job_title']} ({job['job_role']}) requires: {skills}. "
        f"Experience level: {job.get('experience_required') or 'not specified'}."
    )


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _score(required_skills: list[str], candidate_skills: list[str], semantic: float) -> dict:
    required = [s.strip().lower() for s in required_skills]
    candidate = {s.strip().lower() for s in candidate_skills}

    if required:
        matched = [s for s in required if s in candidate]
        missing = [s for s in required if s not in candidate]
        coverage = len(matched) / len(required) * 100
    else:
        matched, missing = [], []
        coverage = 100.0  # nothing specific required -> nothing to fail on

    ai_score = round(0.7 * coverage + 0.3 * semantic)
    ai_score = max(0, min(100, ai_score))

    if coverage >= 90:
        matching_factors = "Strong match"
    elif coverage >= 70:
        matching_factors = "Good match"
    elif coverage >= 40:
        matching_factors = "Skills match"
    else:
        matching_factors = "Skill gaps"

    return {
        "ai_score": ai_score,
        "matching_factors": matching_factors,
        "matched_skills": matched,
        "missing_skills": missing,
        "coverage_percentage": round(coverage),
        "semantic_similarity_percentage": round(semantic),
    }


@tool
def score_match(
    required_skills_json: str, candidate_skills_json: str, semantic_percentage: float
) -> str:
    """Compares a job's required skills against a candidate's skills,
    computes skill coverage, and blends it with an already-computed
    semantic-similarity percentage into the final AI score and
    matching-factors label. `required_skills_json`/`candidate_skills_json`
    are JSON-encoded string lists. Returns the full result as JSON."""
    required_skills = json.loads(required_skills_json)
    candidate_skills = json.loads(candidate_skills_json)
    return json.dumps(_score(required_skills, candidate_skills, semantic_percentage))


class MatchingAgent:
    def __init__(self):
        self._agent = build_tool_agent([score_match], _SYSTEM_PROMPT)

    def run(
        self,
        client: QdrantClient,
        job_id: int,
        job: dict,
        parsed_resume: dict,
        candidate_vector: list[float],
    ) -> dict:
        required_skills = job.get("required_skills", [])
        candidate_skills = parsed_resume.get("skills", [])

        job_text = _job_text(job)
        job_vector = embed_text(job_text)
        client.upsert(
            collection_name=COLLECTION_JOB_REQUIREMENTS,
            points=[
                PointStruct(
                    id=_point_id(job_id),
                    vector=job_vector,
                    payload={"job_id": job_id, "text": job_text},
                )
            ],
        )
        semantic = max(0.0, _cosine_similarity(candidate_vector, job_vector)) * 100

        result = invoke_tool_agent(
            self._agent,
            (
                f"Score this candidate against the job. Required skills: "
                f"{json.dumps(required_skills)}. Candidate skills: "
                f"{json.dumps(candidate_skills)}. Semantic similarity: {semantic}."
            ),
            "score_match",
        )
        return result if result else _score(required_skills, candidate_skills, semantic)
