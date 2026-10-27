"""Agent 8 — Embedding Agent.

phase.md Phase 13: "Converts relevant recruitment/student/company
information into embeddings for semantic retrieval."

Embeds the candidate's parsed evidence and stores it in Qdrant's
`student_evidence` collection — provisioned since Phase 04's Qdrant
collection boundary but used for the first time here — so the resulting
vector is genuinely persisted for semantic retrieval, not just computed
and discarded.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — composing
the evidence text is a `@tool` so it stays exact regardless of whether a
real model is configured (see agent_utils.py's module docstring for the
shared resilience/fallback pattern); the embedding vector itself and the
Qdrant upsert need a live `QdrantClient` and aren't JSON-tool-friendly, so
they stay outside the tool call, built from the tool's text output.
"""

import json
import uuid

from embeddings.model import embed_text
from langchain.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from rag.vector_store import COLLECTION_STUDENT_EVIDENCE

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_NAMESPACE = uuid.UUID("6f6f6c6d-696e-6400-0000-00000000cafe")

_SYSTEM_PROMPT = """
You are the Embedding Agent in LOOP-MIND's AI Recruitment system. Given a
candidate's parsed resume, your job is to call the build_evidence_text
tool to compose the evidence text that will be embedded for semantic
retrieval. Always call the tool — never compose the text yourself.
"""


def _point_id(application_id: int) -> str:
    return str(uuid.uuid5(_NAMESPACE, f"application-evidence|{application_id}"))


def _evidence_text(parsed_resume: dict) -> str:
    parts = [
        "Skills: " + (", ".join(parsed_resume.get("skills", [])) or "none listed"),
        "Projects: " + (", ".join(parsed_resume.get("projects", [])) or "none listed"),
        "Certifications: " + (", ".join(parsed_resume.get("certifications", [])) or "none"),
    ]
    education = parsed_resume.get("education")
    if education:
        parts.append(
            f"Education: {education.get('degree')} in {education.get('branch')} "
            f"at {education.get('college')}"
        )
    return ". ".join(parts)


@tool
def build_evidence_text(parsed_resume_json: str) -> str:
    """Composes the evidence text (skills, projects, certifications,
    education) that will be embedded for semantic retrieval.
    `parsed_resume_json` is a JSON-encoded parsed-resume dict. Returns
    {"embedded_text": ...} as JSON."""
    parsed_resume = json.loads(parsed_resume_json)
    return json.dumps({"embedded_text": _evidence_text(parsed_resume)})


class EmbeddingAgent:
    def __init__(self):
        self._agent = build_tool_agent([build_evidence_text], _SYSTEM_PROMPT)

    def run(self, client: QdrantClient, application_id: int, parsed_resume: dict) -> dict:
        result = invoke_tool_agent(
            self._agent,
            f"Compose the evidence text for this parsed resume: {json.dumps(parsed_resume)}.",
            "build_evidence_text",
        )
        text = result["embedded_text"] if result else _evidence_text(parsed_resume)

        vector = embed_text(text)
        client.upsert(
            collection_name=COLLECTION_STUDENT_EVIDENCE,
            points=[
                PointStruct(
                    id=_point_id(application_id),
                    vector=vector,
                    payload={"application_id": application_id, "text": text},
                )
            ],
        )
        return {"embedded_text": text, "vector": vector}
