"""Agent 7 — Resume Parser Agent.

phase.md Phase 13: "Extracts structured information from student resumes."
Input: Resume PDF. Output: skills, education, projects, experience,
certifications, contact information, other relevant evidence.

Two distinct capabilities live on this one agent (per the UPDATE SDD's
"do not introduce unnecessary additional agents" — this is still Agent 7,
just with its full defined responsibility now implemented):

1. `run(candidate)` — consolidates a candidate's already-stored structured
   evidence (skills, education, projects, certifications, coding
   experience, contact info) into the standard extracted-resume shape.
   Used by Multi-Agent System 2 (recruitment_intelligence.py), where the
   "resume" is the candidate's verified LOOP-MIND record rather than a
   file to read.

2. `extract_from_text(resume_text)` — genuine extraction from the actual
   text of an uploaded resume PDF (read via `pypdf` at the call site in
   backend/services/student_profile_service.py, since "AI services" has
   no `backend`/filesystem dependency of its own — see rag/vector_store.py's
   module docstring). Only returns skills/certifications/projects/education/
   experience information literally present in the text — never invents a
   value, matching the same no-fabrication contract as
   linkedin_extraction_agent.py.

LangChain `create_agent` + Gemini 2.5 Flash (agents/llm.py) — both
capabilities are `@tool`-decorated functions on one shared agent so their
output stays exact regardless of whether a real model is configured; see
agent_utils.py's module docstring for the shared resilience/fallback
pattern.
"""

import json
import re

from langchain.tools import tool

from agents.agent_utils import build_tool_agent, invoke_tool_agent

_SYSTEM_PROMPT = """
You are the Resume Parser Agent in LOOP-MIND's AI Recruitment and Student
Intelligence systems. You have two tools: parse_resume consolidates a
candidate's already-stored structured profile into the standard resume
shape; extract_resume_text extracts skills, certifications, projects,
education, and experience information from the literal text of an
uploaded resume PDF. Use whichever tool matches the request — always call
one of them, never reshape or extract data yourself. Never invent
information that is not present in the input.
"""


def _parse(candidate: dict) -> dict:
    """`candidate` shape: {full_name, email, has_resume_on_file,
    skills: [{skill_name, proficiency, evidence_count}], projects:
    [{project_name}], certifications: [{certification_name}],
    coding_experience: [{programming_languages}], academic:
    {degree, branch, college} | None}."""
    skills = [s["skill_name"] for s in candidate.get("skills", [])]
    evidence_count = sum(s.get("evidence_count", 0) for s in candidate.get("skills", []))

    return {
        "skills": skills,
        "education": candidate.get("academic"),
        "projects": [p["project_name"] for p in candidate.get("projects", [])],
        "experience": candidate.get("coding_experience", []),
        "certifications": [c["certification_name"] for c in candidate.get("certifications", [])],
        "contact_information": {
            "name": candidate.get("full_name"),
            "email": candidate.get("email"),
        },
        "has_resume_on_file": candidate.get("has_resume_on_file", False),
        "evidence_count": evidence_count,
    }


@tool
def parse_resume(candidate_json: str) -> str:
    """Consolidates a candidate's structured profile into the standard
    extracted-resume shape: skills, education, projects, experience,
    certifications, contact information, evidence count.
    `candidate_json` is a JSON-encoded candidate dict. Returns the full
    result as JSON."""
    candidate = json.loads(candidate_json)
    return json.dumps(_parse(candidate))


# ---- Real PDF-text extraction (UPDATE SDD "Student Dashboard" §5/§9) ----

_SECTION_HEADERS = {
    "skills": "skills",
    "technical skills": "skills",
    "key skills": "skills",
    "core competencies": "skills",
    "licenses & certifications": "certifications",
    "licenses and certifications": "certifications",
    "certifications": "certifications",
    "projects": "projects",
    "academic projects": "projects",
    "personal projects": "projects",
    "key projects": "projects",
    "notable projects": "projects",
    "education": "education",
    "academic background": "education",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
}


def _split_resume_sections(text: str) -> dict[str, list[str]]:
    """Blank lines *within* an active section are preserved as `""`
    entries rather than discarded — `_parse_projects` below relies on
    them as project-boundary signals (a blank line between two project
    entries is the strongest available signal that a new project starts
    next). Every other section's own parsing already treats an empty
    line as a no-op (an empty split/strip produces nothing to append),
    so preserving it here doesn't change their behavior."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                sections.setdefault(current, []).append("")
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


# Resume Lifecycle, Exact Resume Parsing, Source-Aware Counts & Agent
# Cross-Check SDD §5-6/§32: "one actual project = one project count" —
# a resume's Projects section typically lists each project as a title
# line followed by attribute lines ("Technologies: React, Node.js,
# MongoDB", "Role: ...", "Description: ..."). Treating every non-empty
# line in that section as its own project (the previous behavior) turned
# a "Technologies: React, Node.js, MongoDB" line into a fake fourth
# project. These prefixes are recognized as *attributes of the current
# project* instead of new projects.
_PROJECT_ATTRIBUTE_KEYS = {
    "technologies": "technologies_used",
    "technology": "technologies_used",
    "tech stack": "technologies_used",
    "techstack": "technologies_used",
    "tools": "technologies_used",
    "stack": "technologies_used",
    "description": "project_description",
    "role": "student_role",
}


def _looks_like_project_title(line: str) -> bool:
    """A short line with no sentence-ending punctuation reads like a
    project name ("E-Commerce Website"); a longer line ending in "." or
    "!" reads like prose describing the project above it ("Built a
    full-stack e-commerce platform with payment integration."). Not
    perfect for every resume's prose style, but a real improvement over
    treating every line as a title regardless of shape."""
    if line.endswith((".", "!")):
        return False
    return len(line.split()) <= 8


def _parse_projects(lines: list[str]) -> list[dict]:
    """`lines` may contain `""` entries marking a blank line in the
    original resume text (see `_split_resume_sections`) — the strongest
    available signal that the next real line starts a new project, used
    together with `_looks_like_project_title` so an unlabeled description
    line directly under a title (no blank line, no "Description:" label)
    is recognized as that project's description rather than becoming a
    fake extra project."""
    projects: list[dict] = []
    current: dict | None = None
    at_boundary = True
    for raw in lines:
        line = raw.strip()
        if not line:
            at_boundary = True
            continue
        # Strip a leading list marker ("1.", "2)", "-", "•") so it never
        # becomes part of the project name.
        stripped = re.sub(r"^(?:\d+[.)]|[-•*])\s*", "", line)

        attribute_match = re.match(r"^([A-Za-z][A-Za-z /]{1,20}?)\s*[:\-—]\s*(.+)$", stripped)
        if attribute_match:
            key = attribute_match.group(1).strip().lower()
            field = _PROJECT_ATTRIBUTE_KEYS.get(key)
            if field and current is not None:
                value = attribute_match.group(2).strip()
                if field == "technologies_used":
                    current[field] = [t.strip() for t in re.split(r"[,/]", value) if t.strip()]
                else:
                    current[field] = value
                at_boundary = False
                continue

        if current is not None and not at_boundary and not _looks_like_project_title(stripped):
            # No blank line separated this from the project above, and it
            # doesn't read like a title — it's a continuation/description
            # of the current project, not a new one.
            existing = current.get("project_description")
            current["project_description"] = (
                f"{existing} {stripped}".strip() if existing else stripped
            )
            at_boundary = False
            continue

        # Anything else starts a new project entity.
        at_boundary = False
        parts = re.split(r"[:—]\s", stripped, maxsplit=1)
        name = parts[0].strip()
        if not name:
            continue
        current = {
            "project_name": name,
            "project_description": parts[1].strip() if len(parts) > 1 else None,
        }
        projects.append(current)
    return projects


_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _extract_email(resume_text: str) -> str | None:
    """Recruiter Interview Invitation & Demo Email Specification §6: the
    email address literally present in the resume text, if any — searched
    across the whole document rather than a specific section, since resumes
    place contact details in a header with no consistent section marker.
    Never invents an address; returns None when none is found."""
    match = _EMAIL_PATTERN.search(resume_text or "")
    return match.group(0) if match else None


def _extract_from_text(resume_text: str) -> dict:
    sections = _split_resume_sections(resume_text or "")

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
        parts = re.split(r"\s[-—]\s", raw, maxsplit=1)
        name = parts[0].strip()
        if name:
            certifications.append(
                {
                    "certification_name": name,
                    "issuing_organization": parts[1].strip() if len(parts) > 1 else None,
                }
            )

    projects = _parse_projects(sections.get("projects", []))

    # Education/experience are surfaced as raw lines only — never mapped
    # onto StudentAcademicInfo's required fields (current_semester,
    # cgpa_scale, admission_year, ...), which a resume never states and
    # which this agent must not fabricate. The caller decides whether any
    # of it is complete enough to persist.
    education_lines = sections.get("education", [])
    experience_lines = sections.get("experience", [])

    return {
        "skills": skills,
        "certifications": certifications,
        "projects": projects,
        "education_lines": education_lines,
        "experience_lines": experience_lines,
        "email": _extract_email(resume_text),
    }


@tool
def extract_resume_text(resume_text: str) -> str:
    """Extracts a candidate's available skills, certifications, and
    projects from the literal text of their resume PDF, plus raw
    education/experience lines and any email address for the caller to
    interpret. Only returns information actually present in the text —
    never invents a value. Returns {"skills", "certifications", "projects",
    "education_lines", "experience_lines", "email"} as JSON."""
    return json.dumps(_extract_from_text(resume_text))


class ResumeParserAgent:
    def __init__(self):
        self._agent = build_tool_agent([parse_resume, extract_resume_text], _SYSTEM_PROMPT)

    def run(self, candidate: dict) -> dict:
        """`candidate` shape: {full_name, email, has_resume_on_file,
        skills: [{skill_name, proficiency, evidence_count}], projects:
        [{project_name}], certifications: [{certification_name}],
        coding_experience: [{programming_languages}], academic:
        {degree, branch, college} | None}."""
        result = invoke_tool_agent(
            self._agent,
            f"Parse this candidate's resume data: {json.dumps(candidate)}.",
            "parse_resume",
        )
        return result if result else _parse(candidate)

    def extract_from_text(self, resume_text: str) -> dict:
        """Extracts skills/certifications/projects/education/experience
        from the actual text of an uploaded resume PDF."""
        result = invoke_tool_agent(
            self._agent,
            f"Extract this resume's available information: {resume_text}",
            "extract_resume_text",
        )
        return result if result else _extract_from_text(resume_text)
