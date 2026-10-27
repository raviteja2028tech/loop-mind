"""Generated Company Intelligence dataset.

spec.md "Company Intelligence, Skill Gap Analysis & Preparation Plan
Specification" §3: "Until an actual company dataset is supplied,
LOOP-MIND must use a generated realistic demonstration Company
Intelligence Dataset... must be treated as demo/synthetic company
intelligence, not as proprietary or officially sourced company data."

Company names here are deliberately fictional rather than real companies
with invented requirements attached — spec.md §30 "No Hallucinated
Company Intelligence" forbids presenting fabricated facts as if they were
a real company's actual hiring criteria. `Company.is_synthetic` keeps the
distinction explicit so a real dataset can replace this one later without
changing the schema (spec.md §4 "Dataset Replacement Architecture").

Idempotent: safe to call on every startup — does nothing once companies
already exist.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.company_intelligence import (
    Company,
    CompanyHistoricalRequirement,
    CompanyRequirementPattern,
    CompanyRoleRequirement,
    SuccessfulCandidateProfile,
)

# Each company: name, industry, description, and 1-2 roles with their
# requirements. Skill proficiency levels use the same vocabulary as the
# student-facing Skill Gap page (Beginner/Intermediate/Advanced).
_COMPANIES = [
    {
        "name": "Nexora Technologies",
        "industry": "Enterprise Software",
        "description": "Cloud-based enterprise productivity platforms.",
        "roles": [
            {
                "role_title": "Software Engineer",
                "required_skills": [
                    {"skill": "Data Structures & Algorithms", "min_proficiency": "Advanced"},
                    {"skill": "System Design", "min_proficiency": "Intermediate"},
                    {"skill": "SQL", "min_proficiency": "Intermediate"},
                    {"skill": "Java", "min_proficiency": "Advanced"},
                ],
                "experience_expectation": "0-2 years or strong academic project history",
                "evidence_expectations": ["GitHub repository", "Deployed project"],
                "project_expectations": ["Backend service with a persistent database"],
            },
            {
                "role_title": "SDE Intern",
                "required_skills": [
                    {"skill": "Data Structures & Algorithms", "min_proficiency": "Intermediate"},
                    {"skill": "Python", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "Pre-final year student",
                "evidence_expectations": ["Any completed coding project"],
                "project_expectations": [],
            },
        ],
        "pattern": (
            "Consistently weights Data Structures & Algorithms heavily "
            "across all engineering roles."
        ),
        "successful_profile": {
            "typical_cgpa": 8.0,
            "common_strengths": ["DSA", "System Design", "Java"],
            "common_projects": ["Full-stack web application", "REST API service"],
        },
    },
    {
        "name": "BluePeak Software",
        "industry": "SaaS",
        "description": "Workflow automation tools for mid-size businesses.",
        "roles": [
            {
                "role_title": "Frontend Developer",
                "required_skills": [
                    {"skill": "JavaScript", "min_proficiency": "Advanced"},
                    {"skill": "React", "min_proficiency": "Advanced"},
                    {"skill": "CSS", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "0-2 years",
                "evidence_expectations": ["Live deployed UI project"],
                "project_expectations": ["Responsive web application"],
            }
        ],
        "pattern": (
            "Prioritizes shipped, deployed UI work over algorithmic depth for frontend roles."
        ),
        "successful_profile": {
            "typical_cgpa": 7.5,
            "common_strengths": ["React", "UI/UX sense", "JavaScript"],
            "common_projects": ["Deployed React application"],
        },
    },
    {
        "name": "Vertex Analytics",
        "industry": "Data & AI",
        "description": "Predictive analytics for the logistics industry.",
        "roles": [
            {
                "role_title": "Data Analyst",
                "required_skills": [
                    {"skill": "SQL", "min_proficiency": "Advanced"},
                    {"skill": "Python", "min_proficiency": "Intermediate"},
                    {"skill": "Statistics", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "0-1 years",
                "evidence_expectations": ["Data analysis project with visualizations"],
                "project_expectations": ["End-to-end analysis notebook or dashboard"],
            }
        ],
        "pattern": "Screens heavily on SQL proficiency before considering any other skill.",
        "successful_profile": {
            "typical_cgpa": 7.8,
            "common_strengths": ["SQL", "Data visualization", "Statistics"],
            "common_projects": ["Dashboard built on a real/public dataset"],
        },
    },
    {
        "name": "CloudArc Systems",
        "industry": "Cloud Infrastructure",
        "description": "Managed Kubernetes and cloud infrastructure tooling.",
        "roles": [
            {
                "role_title": "Backend Developer",
                "required_skills": [
                    {"skill": "System Design", "min_proficiency": "Advanced"},
                    {"skill": "Cloud (AWS/GCP)", "min_proficiency": "Intermediate"},
                    {"skill": "Database / SQL", "min_proficiency": "Advanced"},
                ],
                "experience_expectation": "1-3 years",
                "evidence_expectations": ["Experience with a cloud provider"],
                "project_expectations": ["Service deployed on cloud infrastructure"],
            }
        ],
        "pattern": "Requires demonstrated cloud deployment experience, not just local projects.",
        "successful_profile": {
            "typical_cgpa": 7.6,
            "common_strengths": ["Cloud (AWS/GCP)", "System Design", "Databases"],
            "common_projects": ["Cloud-deployed backend service"],
        },
    },
    {
        "name": "Quantify Labs",
        "industry": "Applied AI",
        "description": "Applied machine learning research and consulting.",
        "roles": [
            {
                "role_title": "ML Engineer",
                "required_skills": [
                    {"skill": "Python", "min_proficiency": "Advanced"},
                    {"skill": "Machine Learning", "min_proficiency": "Advanced"},
                    {"skill": "Data Structures & Algorithms", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "0-2 years, strong ML project portfolio",
                "evidence_expectations": ["Published or deployed ML model"],
                "project_expectations": ["End-to-end ML pipeline"],
            }
        ],
        "pattern": "Weighs project depth in ML over raw CGPA.",
        "successful_profile": {
            "typical_cgpa": 7.2,
            "common_strengths": ["Machine Learning", "Python", "Applied research"],
            "common_projects": ["Trained and deployed ML model"],
        },
    },
    {
        "name": "Ironclad Security",
        "industry": "Cybersecurity",
        "description": "Application security testing and threat monitoring.",
        "roles": [
            {
                "role_title": "Security Engineer",
                "required_skills": [
                    {"skill": "Networking", "min_proficiency": "Advanced"},
                    {"skill": "System Design", "min_proficiency": "Intermediate"},
                    {"skill": "Python", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "1-3 years or strong CTF/security project history",
                "evidence_expectations": ["Security research or CTF participation"],
                "project_expectations": ["Vulnerability research or security tool"],
            }
        ],
        "pattern": (
            "Favors candidates with demonstrated hands-on security practice over coursework alone."
        ),
        "successful_profile": {
            "typical_cgpa": 7.4,
            "common_strengths": ["Networking", "Security tooling"],
            "common_projects": ["CTF participation", "Security scanning tool"],
        },
    },
    {
        "name": "Orbit Robotics",
        "industry": "Robotics",
        "description": "Autonomous navigation systems for warehouse robotics.",
        "roles": [
            {
                "role_title": "Embedded Software Engineer",
                "required_skills": [
                    {"skill": "C++", "min_proficiency": "Advanced"},
                    {"skill": "Data Structures & Algorithms", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "0-2 years",
                "evidence_expectations": ["Hardware/embedded project"],
                "project_expectations": ["Embedded systems or robotics project"],
            }
        ],
        "pattern": "Requires demonstrated C++ depth beyond coursework.",
        "successful_profile": {
            "typical_cgpa": 7.7,
            "common_strengths": ["C++", "Embedded systems"],
            "common_projects": ["Robotics or IoT hardware project"],
        },
    },
    {
        "name": "Fintrust Solutions",
        "industry": "Fintech",
        "description": "Digital lending and payments infrastructure.",
        "roles": [
            {
                "role_title": "Backend Developer",
                "required_skills": [
                    {"skill": "Java", "min_proficiency": "Advanced"},
                    {"skill": "Database / SQL", "min_proficiency": "Advanced"},
                    {"skill": "System Design", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "1-3 years",
                "evidence_expectations": ["Experience with transactional systems"],
                "project_expectations": ["Project involving data integrity/consistency"],
            }
        ],
        "pattern": "Places unusually high weight on data-consistency-aware system design.",
        "successful_profile": {
            "typical_cgpa": 7.9,
            "common_strengths": ["Java", "Databases", "System Design"],
            "common_projects": ["Transactional backend system"],
        },
    },
    {
        "name": "Northwind Retail Tech",
        "industry": "E-commerce",
        "description": "E-commerce platform and logistics software.",
        "roles": [
            {
                "role_title": "Full Stack Developer",
                "required_skills": [
                    {"skill": "JavaScript", "min_proficiency": "Advanced"},
                    {"skill": "Node.js", "min_proficiency": "Intermediate"},
                    {"skill": "SQL", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "0-2 years",
                "evidence_expectations": ["Full-stack deployed project"],
                "project_expectations": ["E-commerce-style project with cart/checkout flow"],
            }
        ],
        "pattern": "Prefers breadth (full stack) over deep specialization for early-career roles.",
        "successful_profile": {
            "typical_cgpa": 7.3,
            "common_strengths": ["Full-stack development", "JavaScript"],
            "common_projects": ["Deployed full-stack web application"],
        },
    },
    {
        "name": "Skyline Mobility",
        "industry": "Mobile Apps",
        "description": "Consumer ride-sharing and delivery mobile apps.",
        "roles": [
            {
                "role_title": "Mobile App Developer",
                "required_skills": [
                    {"skill": "Kotlin", "min_proficiency": "Intermediate"},
                    {"skill": "Data Structures & Algorithms", "min_proficiency": "Intermediate"},
                ],
                "experience_expectation": "0-2 years",
                "evidence_expectations": ["Published or side-loadable mobile app"],
                "project_expectations": ["Mobile application with a backend integration"],
            }
        ],
        "pattern": "Values a shipped app (even side-loaded) over unpublished coursework projects.",
        "successful_profile": {
            "typical_cgpa": 7.1,
            "common_strengths": ["Mobile development", "API integration"],
            "common_projects": ["Published or demoed mobile app"],
        },
    },
]


def seed_company_intelligence(db: Session) -> None:
    if db.scalar(select(Company).limit(1)) is not None:
        return

    for entry in _COMPANIES:
        company = Company(
            name=entry["name"],
            industry=entry["industry"],
            description=entry["description"],
            is_synthetic=True,
        )
        db.add(company)
        db.flush()  # assign company.id

        for role in entry["roles"]:
            db.add(
                CompanyRoleRequirement(
                    company_id=company.id,
                    role_title=role["role_title"],
                    required_skills=role["required_skills"],
                    experience_expectation=role["experience_expectation"],
                    evidence_expectations=role["evidence_expectations"],
                    project_expectations=role["project_expectations"],
                )
            )
            db.add(
                CompanyHistoricalRequirement(
                    company_id=company.id,
                    role_title=role["role_title"],
                    cycle_year=2025,
                    requirement_snapshot={"required_skills": role["required_skills"]},
                )
            )

        db.add(
            CompanyRequirementPattern(
                company_id=company.id,
                pattern_description=entry["pattern"],
                pattern_data={},
            )
        )
        db.add(
            SuccessfulCandidateProfile(
                company_id=company.id,
                role_title=entry["roles"][0]["role_title"],
                profile_summary=entry["successful_profile"],
            )
        )

    db.commit()
