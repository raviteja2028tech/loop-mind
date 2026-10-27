"""Shared skill/requirement lookup helpers — used by both the Skill Gap
Analysis page (Phase 08) and the Preparation Plan page (Phase 09) to turn
raw stored data into the same skill-domain categories and current/required
proficiency levels, so both pages agree on what a skill "is" and where the
student currently stands against a target role.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.company_intelligence import Company
from backend.models.student_profile import StudentSkill

# Presentational fallback only — used when a required skill isn't (yet) in
# the student's own profile, so it has no stored category of its own.
# spec.md's own example categories (Core CS, System Design, Cloud,
# Database, Web Development) are the keys' targets here.
_SKILL_CATEGORY = {
    "data structures & algorithms": "Core CS",
    "system design": "System Design",
    "sql": "Database",
    "database": "Database",
    "java": "Core CS",
    "python": "Core CS",
    "javascript": "Web Development",
    "react": "Web Development",
    "css": "Web Development",
    "node.js": "Web Development",
    "html": "Web Development",
    "aws": "Cloud",
    "gcp": "Cloud",
    "cloud (aws/gcp)": "Cloud",
    "docker": "Cloud",
    "kubernetes": "Cloud",
    "machine learning": "Data / ML",
    "deep learning": "Data / ML",
    "data analysis": "Data / ML",
    "networking": "Systems",
    "security": "Security",
    "embedded systems": "Systems",
    "c++": "Core CS",
    "c": "Core CS",
}


def category_for(skill_name: str) -> str:
    return _SKILL_CATEGORY.get(skill_name.strip().lower(), "General")


def required_levels_for(db: Session, company_name: str, role_title: str | None) -> dict[str, str]:
    company = db.scalar(select(Company).where(Company.name == company_name))
    if company is None:
        return {}
    requirement = next((r for r in company.role_requirements if r.role_title == role_title), None)
    if requirement is None:
        return {}
    return {
        item["skill"].strip().lower(): item["min_proficiency"]
        for item in requirement.required_skills
    }


def student_skill_lookup(db: Session, student_id: int) -> dict[str, tuple[str, str]]:
    skills = db.scalars(select(StudentSkill).where(StudentSkill.student_id == student_id))
    return {s.skill_name.strip().lower(): (s.skill_category, s.proficiency) for s in skills}
