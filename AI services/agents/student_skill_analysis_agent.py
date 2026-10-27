"""Agent 2 — Student Skill Analysis Agent.

phase.md Phase 06: analyzes student skills, academics, projects,
certifications, coding experience, evidence, current learning status.
spec.md §2.2: "The system evaluates evidence, not just claimed skills" —
this is why every skill carries an `evidence_count`.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — the
analysis itself is a `@tool` so its output stays exact regardless of
whether a real model is configured; see agent_utils.py's module docstring
for the shared resilience/fallback pattern.
"""

import json

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the Student Skill Analysis Agent in LOOP-MIND's Student
Intelligence system. Given a student's profile, your job is to call the
analyze_student tool to identify their strong skills, skills lacking
evidence, and activity counts. Always call the tool — never analyze the
profile yourself.
"""


def _analyze(student: dict) -> dict:
    """`student` shape: {student_id, skills: [{skill_name,
    skill_category, proficiency, learning_status, experience_years,
    evidence_count}], projects: [...], certifications: [...],
    coding_experience: [...], academic: {...} | None}."""
    skills = student.get("skills", [])
    strong_skills = [s["skill_name"] for s in skills if s["proficiency"] == "Advanced"]
    skills_without_evidence = [s["skill_name"] for s in skills if s.get("evidence_count", 0) == 0]

    return {
        "student_id": student["student_id"],
        "skills": skills,
        "strong_skills": strong_skills,
        "skills_without_evidence": skills_without_evidence,
        "project_count": len(student.get("projects", [])),
        "certification_count": len(student.get("certifications", [])),
        "coding_experience_count": len(student.get("coding_experience", [])),
        "academic": student.get("academic"),
    }


@tool
def analyze_student(student_json: str) -> str:
    """Analyzes a student's profile: identifies skills at Advanced
    proficiency, skills with no supporting evidence, and counts of
    projects/certifications/coding experience. `student_json` is a
    JSON-encoded student dict. Returns the full analysis as JSON."""
    student = json.loads(student_json)
    return json.dumps(_analyze(student))


class StudentSkillAnalysisAgent:
    def __init__(self):
        self._agent = build_tool_agent([analyze_student], _SYSTEM_PROMPT)

    def run(self, student: dict) -> dict:
        """`student` shape: {student_id, skills: [{skill_name,
        skill_category, proficiency, learning_status, experience_years,
        evidence_count}], projects: [...], certifications: [...],
        coding_experience: [...], academic: {...} | None}."""
        result = invoke_tool_agent(
            self._agent,
            f"Analyze this student's profile: {json.dumps(student)}.",
            "analyze_student",
        )
        return result if result else _analyze(student)
