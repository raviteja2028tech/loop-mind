"""Sentence-Transformers embedding loader — spec.md "Embeddings: Sentence
Transformers". Single shared model instance (~80MB, all-MiniLM-L6-v2,
384-dim) matching the dimension configured in rag/vector_store.py.
"""

_model = None


def get_embedding_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    model = get_embedding_model()
    return model.encode(texts, normalize_embeddings=True).tolist()


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]
