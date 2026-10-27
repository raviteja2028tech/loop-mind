"""Semantic retrieval over the `company_knowledge` collection — the "RAG"
half of spec.md's "Embeddings -> Qdrant -> RAG -> LangChain Agents" flow.
Used by the Company Intelligence Agent to pull supporting context
(patterns, successful-candidate narratives) beyond the exact structured
row lookup, for the reasoning text it produces.
"""

from embeddings.model import embed_text
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

from rag.vector_store import COLLECTION_COMPANY_KNOWLEDGE


def search_company_knowledge(
    client: QdrantClient,
    query: str,
    *,
    company_id: int | None = None,
    top_k: int = 5,
) -> list[dict]:
    """Returns up to `top_k` chunks as [{text, score, source_type,
    role_title}], optionally restricted to one company via a Qdrant
    payload filter."""
    query_filter = None
    if company_id is not None:
        query_filter = Filter(
            must=[FieldCondition(key="company_id", match=MatchValue(value=company_id))]
        )

    results = client.query_points(
        collection_name=COLLECTION_COMPANY_KNOWLEDGE,
        query=embed_text(query),
        query_filter=query_filter,
        limit=top_k,
    ).points

    return [
        {
            "text": point.payload.get("text", ""),
            "score": point.score,
            "source_type": point.payload.get("source_type"),
            "role_title": point.payload.get("role_title"),
        }
        for point in results
    ]
