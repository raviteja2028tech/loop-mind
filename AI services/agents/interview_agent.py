"""Agent 11 — Interview Agent.

phase.md Phase 15: triggered after recruiter approval. Identifies the
specific job role, understands its real required skills, and generates
role-specific interview questions — never one generic question set reused
for every candidate/job — plus the evaluation criteria/rubric for each
question (spec.md: "The source also defines: evaluation criteria;
rubrics").

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — question
generation is a `@tool` so the output stays exact regardless of whether a
real model is configured; see agent_utils.py's module docstring for the
shared resilience/fallback pattern.
"""

import json

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the Interview Agent in LOOP-MIND's AI Recruitment system. Given a
job role and its actual required skills, your job is to call the
generate_questions tool to produce one skill-specific interview question
per required skill plus generic role-fit questions, each with its
evaluation criteria. Always call the tool — never invent questions
yourself.
"""

_GENERIC_QUESTIONS = [
    (
        "Walk us through your background and what draws you to the {job_role} role.",
        "Background",
        "Looks for genuine motivation and relevant prior experience.",
    ),
    (
        "Describe a challenging problem you solved recently and how you approached it.",
        "Problem Solving",
        "Looks for structured thinking, ownership of the outcome, and clear communication.",
    ),
]


def _generate(job_role: str, required_skills: list[str]) -> list[dict]:
    """Returns [{question_text, category, evaluation_criteria}, ...] —
    one skill-specific question per the job's actual required skill, plus
    generic role-fit questions."""
    questions = []
    for skill in required_skills:
        questions.append(
            {
                "question_text": (
                    f"Describe a situation where you applied {skill}, and explain "
                    "the approach you took."
                ),
                "category": skill,
                "evaluation_criteria": (
                    f"Looks for genuine hands-on experience with {skill}, clear "
                    "reasoning, and awareness of trade-offs or limitations."
                ),
            }
        )

    for template, category, criteria in _GENERIC_QUESTIONS:
        questions.append(
            {
                "question_text": template.format(job_role=job_role),
                "category": category,
                "evaluation_criteria": criteria,
            }
        )

    return questions


@tool
def generate_questions(job_role: str, required_skills_json: str) -> str:
    """Generates role-specific interview questions (one per required
    skill, plus generic role-fit questions), each with its evaluation
    criteria. `required_skills_json` is a JSON-encoded list of skill
    names; returns the full question list as JSON."""
    required_skills = json.loads(required_skills_json)
    return json.dumps(_generate(job_role, required_skills))


class InterviewAgent:
    def __init__(self):
        self._agent = build_tool_agent([generate_questions], _SYSTEM_PROMPT)

    def run(self, job_role: str, required_skills: list[str]) -> list[dict]:
        """Returns [{question_text, category, evaluation_criteria}, ...] —
        one skill-specific question per the job's actual required skill,
        plus generic role-fit questions."""
        result = invoke_tool_agent(
            self._agent,
            (
                f"Generate interview questions for the {job_role} role. "
                f"Required skills: {json.dumps(required_skills)}."
            ),
            "generate_questions",
        )
        return result if result else _generate(job_role, required_skills)
