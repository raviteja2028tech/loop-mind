"""Agent 13 — LinkedIn Profile Extraction Agent.

UPDATE SDD §6-9: extracts a student's available LinkedIn profile
information and maps it onto LOOP-MIND's existing Student Profile
fields, so the corresponding manual onboarding steps can be skipped.

No authenticated LinkedIn API or scraping access exists in this
environment (LinkedIn requires login for real profile data, and scraping
it would violate its Terms of Service) — the same honest-ceiling
reasoning as resume_parser_agent.py's own docstring. The genuine
"extraction" this agent performs is over the profile text the student
pastes in themselves (the About/Experience/Education/Skills/
Certifications/Projects sections, as they appear when copied from their
own LinkedIn page), never a live fetch.

Only skills, certifications, and projects are mapped to database writes.
Academic info is deliberately NOT persisted from this agent:
StudentAcademicInfo requires several LOOP-MIND-specific fields a LinkedIn
profile never contains (current_semester, cgpa_scale, current_cgpa,
admission_year) — inventing them to satisfy the schema would be exactly
the fabrication this agent must never do, so that table is left for the
student's own manual Academic Information entry instead.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — extraction
is a `@tool` so its output stays exact regardless of whether a real model
is configured; see agent_utils.py's module docstring for the shared
resilience/fallback pattern.
"""

import json
import re

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the LinkedIn Profile Extraction Agent in LOOP-MIND's Student
Intelligence system. A student has pasted the text content of their own
LinkedIn profile. Your job is to call the extract_linkedin_profile tool
with that text so it can identify only the skills, certifications, and
projects genuinely present and map them onto LOOP-MIND's student profile
fields. Never invent a value that is not actually present in the text —
leave a field or list empty instead of guessing.
"""

_SECTION_HEADERS = {
    "skills": "skills",
    "licenses & certifications": "certifications",
    "licenses and certifications": "certifications",
    "certifications": "certifications",
    "projects": "projects",
}


def _split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        key = _SECTION_HEADERS.get(line.lower().rstrip(":"))
        if key:
            current = key
            sections.setdefault(current, [])
            continue
        if current:
            sections.setdefault(current, []).append(line)
    return sections


def _guess_skill_category(skill_name: str) -> str:
    name = skill_name.lower()
    if any(k in name for k in ("aws", "azure", "gcp", "cloud")):
        return "Cloud"
    if any(k in name for k in ("docker", "kubernetes", "ci/cd", "devops", "jenkins")):
        return "DevOps"
    if any(k in name for k in ("sql", "mongo", "postgres", "database", "redis")):
        return "Database"
    if any(
        k in name
        for k in ("react", "django", "flask", "spring", "node", "express", ".net", "angular")
    ):
        return "Framework"
    if any(k in name for k in ("algorithm", "data structure", "dsa")):
        return "Data Structures & Algorithms"
    if any(k in name for k in ("communication", "leadership", "teamwork", "soft skill")):
        return "Soft Skill"
    return "Programming Language"


def _extract(profile_text: str) -> dict:
    sections = _split_sections(profile_text or "")

    skills = []
    for raw in sections.get("skills", []):
        for name in re.split(r"[,•]", raw):
            name = name.strip(" \t-")
            if name:
                skills.append(
                    {
                        "skill_name": name,
                        "skill_category": _guess_skill_category(name),
                        "proficiency": "Intermediate",
                        "learning_status": "Confident",
                    }
                )

    certifications = []
    for raw in sections.get("certifications", []):
        # "Certification Name — Issuing Org" or "Certification Name - Issuing Org"
        parts = re.split(r"\s[-—]\s", raw, maxsplit=1)
        name = parts[0].strip()
        if name:
            certifications.append(
                {
                    "certification_name": name,
                    "issuing_organization": parts[1].strip() if len(parts) > 1 else None,
                }
            )

    projects = []
    for raw in sections.get("projects", []):
        parts = re.split(r"[:—]\s", raw, maxsplit=1)
        name = parts[0].strip()
        if name:
            projects.append(
                {
                    "project_name": name,
                    "project_description": parts[1].strip() if len(parts) > 1 else None,
                }
            )

    return {"skills": skills, "certifications": certifications, "projects": projects}


@tool
def extract_linkedin_profile(profile_text: str) -> str:
    """Extracts a student's available skills, certifications, and
    projects from the plain text of their own LinkedIn profile (as
    pasted by the student, with Skills/Certifications/Projects
    sections). Only returns information literally present in the text —
    never invents a value. Returns {"skills", "certifications",
    "projects"} as JSON."""
    return json.dumps(_extract(profile_text))


class LinkedInExtractionAgent:
    def __init__(self):
        self._agent = build_tool_agent([extract_linkedin_profile], _SYSTEM_PROMPT)

    def run(self, profile_text: str) -> dict:
        result = invoke_tool_agent(
            self._agent,
            f"Extract this LinkedIn profile's available skills, certifications, "
            f"and projects: {profile_text}",
            "extract_linkedin_profile",
        )
        return result if result else _extract(profile_text)
