"""Agent 12 — Email Agent.

phase.md Phase 15: handles interview invitation, interview information,
interview-related email, and candidate communication.

No real email-sending provider is configured in this environment (the
same situation as OTP delivery — spec.md's own dev-mode for that already
establishes the precedent of surfacing generated content directly rather
than silently pretending to dispatch it). This agent produces the
invitation's subject/body from the real candidate/job/schedule data; the
Interviews page shows that content to the recruiter rather than sending
it through an actual mail transport.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — the message
composition itself is a `@tool` so its output stays exact regardless of
whether a real model is configured; see agent_utils.py's module docstring
for the shared resilience/fallback pattern.
"""

import json

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the Email Agent in LOOP-MIND's AI Recruitment system. Given
candidate, job, company, and interview schedule details, your job is to
call the compose_invitation tool to produce the interview invitation's
subject and body. Always call the tool — never compose the message
yourself.
"""


def _compose(
    candidate_name: str,
    job_title: str,
    job_role: str,
    company_name: str,
    interview_type: str,
    scheduled_at_display: str,
    matched_skills: list[str] | None = None,
) -> dict:
    # Recruiter Dashboard — Final Specification §7: explain *why* the
    # candidate was selected using the recruitment pipeline's own actual
    # matching data — never a generic "your profile matches our
    # requirements" line, and never a skill that isn't genuinely present
    # in the stored evaluation. When no matched-skills data exists (e.g.
    # an older application evaluated before this field existed), this
    # paragraph is simply omitted rather than inventing one.
    skills_clause = ""
    if matched_skills:
        skills_list = "\n".join(f"- {skill}" for skill in matched_skills)
        skills_clause = (
            "\nYour profile was selected based on your demonstrated skills relevant to this "
            f"role, including:\n{skills_list}\n"
        )

    subject = f"Interview Invitation — {job_title} at {company_name}"
    body = (
        f"Hi {candidate_name},\n\n"
        f"Congratulations! You have been shortlisted for the {job_role} role "
        f"({job_title}) at {company_name}.\n"
        f"{skills_clause}\n"
        f"We would like to invite you to a {interview_type} interview for this position, "
        f"scheduled for {scheduled_at_display}.\n\n"
        "We look forward to speaking with you.\n\n"
        f"— {company_name} Hiring Team"
    )
    return {"subject": subject, "body": body}


@tool
def compose_invitation(
    candidate_name: str,
    job_title: str,
    job_role: str,
    company_name: str,
    interview_type: str,
    scheduled_at_display: str,
    matched_skills_json: str = "[]",
) -> str:
    """Composes an interview invitation's subject and body from candidate,
    job, company, and schedule details, explaining the selection using the
    actual matched skills from the recruitment pipeline's evaluation
    (`matched_skills_json`, a JSON-encoded list — may be empty). Returns
    {"subject", "body"} as JSON."""
    matched_skills = json.loads(matched_skills_json)
    return json.dumps(
        _compose(
            candidate_name,
            job_title,
            job_role,
            company_name,
            interview_type,
            scheduled_at_display,
            matched_skills,
        )
    )


class EmailAgent:
    def __init__(self):
        self._agent = build_tool_agent([compose_invitation], _SYSTEM_PROMPT)

    def generate_interview_invitation(
        self,
        *,
        candidate_name: str,
        job_title: str,
        job_role: str,
        company_name: str,
        interview_type: str,
        scheduled_at_display: str,
        matched_skills: list[str] | None = None,
    ) -> dict:
        matched_skills = matched_skills or []
        result = invoke_tool_agent(
            self._agent,
            (
                f"Compose an interview invitation for {candidate_name} — {job_title} "
                f"({job_role}) at {company_name}, a {interview_type} interview scheduled "
                f"for {scheduled_at_display}. Skills that contributed to their selection: "
                f"{json.dumps(matched_skills)}."
            ),
            "compose_invitation",
        )
        return (
            result
            if result
            else _compose(
                candidate_name,
                job_title,
                job_role,
                company_name,
                interview_type,
                scheduled_at_display,
                matched_skills,
            )
        )
