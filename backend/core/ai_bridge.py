"""Bridges the backend to the "AI services" and "ML and DL" packages.

Both directory names contain a space (spec.md's literal repository
structure), so they can never be `import`ed as packages themselves —
Python identifiers can't contain spaces. Instead, this module appends
each directory to `sys.path`, so their *subdirectories* (agents/,
multi_agent/, rag/, embeddings/, ml/, dl/, ...) become importable as
ordinary top-level packages, e.g. `from agents.llm import ...`.

Import this module (for its side effect) before importing anything from
those packages — every call site does `from backend.core.ai_bridge import
ensure_ai_services_importable` and calls it first.

Append, never insert(0, ...): "AI services/email/" is a real, empty
package required by spec.md's repository structure, and if it were
placed ahead of the standard library on sys.path it silently shadows
Python's own stdlib `email` package — which `importlib.metadata` (and
therefore LangChain) imports internally. Appending means the standard
library and every installed dependency always resolve first; our
directories are consulted only as a last resort, exactly the guarantee
that avoids this collision (and any similar one).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_SERVICES_DIR = REPO_ROOT / "AI services"
ML_AND_DL_DIR = REPO_ROOT / "ML and DL"

_done = False


def ensure_ai_services_importable() -> None:
    global _done
    if _done:
        return
    for directory in (AI_SERVICES_DIR, ML_AND_DL_DIR):
        path_str = str(directory)
        if path_str not in sys.path:
            sys.path.append(path_str)
    _done = True
