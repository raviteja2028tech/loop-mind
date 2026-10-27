"""LangChain model initialization — shared by every LOOP-MIND agent.

spec.md's LLM requirement: Google Gemini 2.5 Flash, accessed through the
LangChain layer so the underlying model can be changed without
redesigning the application. `get_model()` is that one shared
initialization point — every agent calls this, never `init_chat_model`
directly, so the model can still be swapped in exactly one place.

The key is read from the repo-root `.env` (`GOOGLE_API_KEY`), never
hardcoded — "AI services" stays free of any `backend` dependency (see
rag/vector_store.py's module docstring for why), so it loads the .env
file itself via `python-dotenv` rather than going through backend's
pydantic-settings config.
"""

from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

_REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_REPO_ROOT / ".env")

_MODEL_ID = "google_genai:gemini-2.5-flash"

_shared_model: BaseChatModel | None = None
_attempted_init = False


def get_model() -> BaseChatModel | None:
    """The one shared Gemini 2.5 Flash instance every agent's
    `create_agent(...)` uses as its `model=`.

    Returns `None` — rather than raising — when no `GOOGLE_API_KEY` is
    configured yet (or construction otherwise fails), since
    `langchain-google-genai` validates the key eagerly at construction
    time, before any network call. Each agent treats `None` as "run the
    deterministic fallback for every call" (see agent_utils.py), the same
    resilience contract as if a real call had failed at invocation time."""
    global _shared_model, _attempted_init
    if _shared_model is None and not _attempted_init:
        _attempted_init = True
        try:
            _shared_model = init_chat_model(_MODEL_ID)
        except Exception:
            _shared_model = None
    return _shared_model
