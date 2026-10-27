"""Qdrant vector-data architecture — spec.md Phase 04 "Qdrant data
boundary" + "FINAL BUILD TECHNOLOGY & AI SPECIFICATION" §4/§7.

This module only *prepares* the architecture (client + collections with
the correct vector configuration). Actual embedding/ingestion lives in
rag/ingest.py and retrieval in rag/retrieve.py (Phase 06), using the
Sentence-Transformers model named below.

Standalone by design: this lives under "AI services/" (a directory name
with a space, so it cannot be `import`ed as a Python package via normal
syntax) and is meant to be run directly —

    python "AI services/rag/vector_store.py"

or invoked by path via `importlib.util.spec_from_file_location` — rather
than imported as `AI_services.rag.vector_store`. It intentionally does
not depend on the `backend` package so it can be run and tested in
isolation.

SQLite remains the source of truth for all structured data (spec.md §3:
"Qdrant should not become the authoritative database for users,
applications, jobs, approvals, etc."). Qdrant only ever holds embeddings
+ metadata pointing back to a SQLite row.
"""

from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

REPO_ROOT = Path(__file__).resolve().parents[2]
QDRANT_STORAGE_PATH = REPO_ROOT / "databases" / "qdrant" / "local"

# all-MiniLM-L6-v2 (Sentence-Transformers) — small, fast, 384-dim. This is
# LOOP-MIND's standard embedding model until a different one is specified.
EMBEDDING_DIMENSIONS = 384

# spec.md Phase 04 "Qdrant data boundary" — exactly these 9 collections.
COLLECTION_COMPANY_KNOWLEDGE = "company_knowledge"
COLLECTION_JOB_REQUIREMENTS = "job_requirements"
COLLECTION_HISTORICAL_RECRUITMENT_INFORMATION = "historical_recruitment_information"
COLLECTION_SUCCESSFUL_CANDIDATE_INFORMATION = "successful_candidate_information"
COLLECTION_STUDENT_EVIDENCE = "student_evidence"
COLLECTION_SKILL_KNOWLEDGE = "skill_knowledge"
COLLECTION_INTERVIEW_KNOWLEDGE = "interview_knowledge"
COLLECTION_PREPARATION_RESOURCES = "preparation_resources"
COLLECTION_RECRUITMENT_OUTCOMES = "recruitment_outcomes"

COLLECTIONS = [
    COLLECTION_COMPANY_KNOWLEDGE,
    COLLECTION_JOB_REQUIREMENTS,
    COLLECTION_HISTORICAL_RECRUITMENT_INFORMATION,
    COLLECTION_SUCCESSFUL_CANDIDATE_INFORMATION,
    COLLECTION_STUDENT_EVIDENCE,
    COLLECTION_SKILL_KNOWLEDGE,
    COLLECTION_INTERVIEW_KNOWLEDGE,
    COLLECTION_PREPARATION_RESOURCES,
    COLLECTION_RECRUITMENT_OUTCOMES,
]


def get_client() -> QdrantClient:
    """Local/embedded Qdrant — no server process required (Docker stays
    optional per spec.md's tech-stack decision)."""
    QDRANT_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    return QdrantClient(path=str(QDRANT_STORAGE_PATH))


def ensure_collections(client: QdrantClient) -> list[str]:
    """Create any missing collection with the standard vector config.
    Idempotent — existing collections are left untouched. Returns the
    names of collections that were newly created."""
    existing = {c.name for c in client.get_collections().collections}
    created = []
    for name in COLLECTIONS:
        if name in existing:
            continue
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE),
        )
        created.append(name)
    return created


if __name__ == "__main__":
    qdrant = get_client()
    newly_created = ensure_collections(qdrant)
    all_collections = sorted(c.name for c in qdrant.get_collections().collections)
    print(f"Qdrant storage: {QDRANT_STORAGE_PATH}")
    print(f"Created: {newly_created or 'none (already existed)'}")
    print(f"All collections: {all_collections}")
    qdrant.close()
