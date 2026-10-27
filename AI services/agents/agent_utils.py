"""Shared `create_agent` invocation helper — every LOOP-MIND agent uses
this so the tool-call-extraction and resilience logic lives in one place.

Resilience pattern: if the real Gemini call fails for any reason (no
`GOOGLE_API_KEY` configured yet, network error, rate limit, malformed
response), `invoke_tool_agent` returns `None` rather than raising — each
agent's own `run()` then falls back to calling its tool function directly
so the deterministic result is identical either way. This mirrors the
project's existing dev-mode fallback pattern (OTP's `dev_otp`, the
previous `TemplateChatModel` stand-in): the system stays fully functional
and testable before a real key is configured, and starts using genuine
Gemini reasoning the moment one is, with no further code changes.
"""

import json
from typing import Any

from langchain.agents import create_agent
from langchain_core.messages import ToolMessage

from agents.llm import get_model


def build_tool_agent(tools: list, system_prompt: str) -> Any | None:
    """Every agent's `create_agent(model=get_model(), tools=[...],
    system_prompt=..., debug=True)` call, in one place — returns `None`
    instead of constructing an agent around a missing model, so
    `invoke_tool_agent` below can uniformly treat "no agent" as "run the
    deterministic fallback"."""
    model = get_model()
    if model is None:
        return None
    return create_agent(model=model, tools=tools, system_prompt=system_prompt, debug=True)


def invoke_tool_agent(agent: Any | None, user_message: str, tool_name: str) -> dict | None:
    """Invokes a `create_agent(...)` agent with a single user message and
    returns the parsed JSON the named tool actually returned — the tool's
    own return value, not the LLM's paraphrase of it, so the structured
    data downstream code relies on stays exact. Returns `None` if no
    agent was constructed (e.g. no API key configured yet — see
    llm.py's `get_model()`), the call failed, or it never invoked the
    tool — the caller's deterministic fallback covers every case alike."""
    if agent is None:
        return None
    try:
        response = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    except Exception:
        return None

    for message in reversed(response.get("messages", [])):
        if isinstance(message, ToolMessage) and message.name == tool_name:
            try:
                return json.loads(message.content)
            except (TypeError, ValueError):
                return None
    return None
