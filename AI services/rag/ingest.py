"""Embeds Company Intelligence records into Qdrant's `company_knowledge`
collection — spec.md RAG flow: "Company / Recruitment / Student Data ->
Data Processing -> Embeddings -> Qdrant -> RAG -> LangChain Agents".

Deliberately takes plain dicts rather than SQLAlchemy models: this
package has no dependency on `backend` (see vector_store.py's module
docstring) — the caller (backend/services/intelligence_service.py) reads
SQLite and shapes the data into the dict form documented below.

Idempotent: point IDs are deterministic (uuid5 of a stable key), so
re-ingesting the same company updates its vectors instead of duplicating
them.
"""

import uuid

from embeddings.model import embed_texts
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from rag.vector_store import COLLECTION_COMPANY_KNOWLEDGE

_NAMESPACE = uuid.UUID("6f6f6c6d-696e-6400-0000-00000000cafe")


def _point_id(*parts: str) -> str:
    return str(uuid.uuid5(_NAMESPACE, "|".join(parts)))


def company_to_chunks(company: dict) -> list[dict]:
    """company: {company_id, company_name, industry, role_requirements:
    [{role_title, required_skills:[{skill,min_proficiency}],
    experience_expectation, evidence_expectations, project_expectations}],
    patterns: [str], successful_candidate_profiles: [{role_title,
    profile_summary}]}. Returns [{id, text, payload}]."""
    chunks = []
    name = company["company_name"]
    cid = str(company["company_id"])

    for role in company.get("role_requirements", []):
        skills = ", ".join(
            f"{s['skill']} ({s.get('min_proficiency', 'Beginner')})"
            for s in role.get("required_skills", [])
        )
        evidence = ", ".join(role.get("evidence_expectations", [])) or "none specified"
        text = (
            f"{name} — {role['role_title']} requires: {skills}. "
            f"Experience expectation: {role.get('experience_expectation') or 'not specified'}. "
            f"Evidence expected: {evidence}."
        )
        chunks.append(
            {
                "id": _point_id("role_requirement", cid, role["role_title"]),
                "text": text,
                "payload": {
                    "source_type": "role_requirement",
                    "company_id": company["company_id"],
                    "company_name": name,
                    "role_title": role["role_title"],
                },
            }
        )

    for pattern in company.get("patterns", []):
        chunks.append(
            {
                "id": _point_id("pattern", cid, pattern[:80]),
                "text": f"{name} recruitment pattern: {pattern}",
                "payload": {
                    "source_type": "requirement_pattern",
                    "company_id": company["company_id"],
                    "company_name": name,
                },
            }
        )

    for profile in company.get("successful_candidate_profiles", []):
        summary = profile.get("profile_summary", {})
        text = (
            f"{name} successful candidates for {profile.get('role_title') or 'this role'} "
            f"typically show: {summary}"
        )
        chunks.append(
            {
                "id": _point_id("successful_profile", cid, str(profile.get("role_title"))),
                "text": text,
                "payload": {
                    "source_type": "successful_candidate_profile",
                    "company_id": company["company_id"],
                    "company_name": name,
                    "role_title": profile.get("role_title"),
                },
            }
        )

    return chunks


def ingest_companies(client: QdrantClient, companies: list[dict]) -> int:
    """Embeds and upserts every chunk for the given companies into the
    `company_knowledge` collection. Returns the number of chunks written."""
    all_chunks = [chunk for company in companies for chunk in company_to_chunks(company)]
    if not all_chunks:
        return 0

    vectors = embed_texts([c["text"] for c in all_chunks])
    points = [
        PointStruct(
            id=chunk["id"], vector=vector, payload={**chunk["payload"], "text": chunk["text"]}
        )
        for chunk, vector in zip(all_chunks, vectors, strict=True)
    ]
    client.upsert(collection_name=COLLECTION_COMPANY_KNOWLEDGE, points=points)
    return len(points)
