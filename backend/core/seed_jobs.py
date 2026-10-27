"""Development/demo Job postings — phase.md Phase 10.

Job creation is a Recruiter Portal feature (Phase 12, "Job Management &
Create New Job") that does not exist yet, so — mirroring the same
already-established pattern as backend/core/seed_company_intelligence.py
("Generated Synthetic Company Dataset... Development / Testing... Same
Processing Architecture" once real data exists) — a small generated set of
job postings is seeded under the demo recruiter account so the Jobs page
has real, varied, database-driven data to search/filter/apply against
before recruiters can post their own. Reuses the same fictional company
names as the Company Intelligence dataset for narrative consistency;
never real companies.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.seed import DEMO_RECRUITER_MOBILE
from backend.models.jobs import Job
from backend.models.recruiter import Recruiter

_JOBS = [
    {
        "company_name": "Nexora Technologies",
        "job_title": "Software Engineer",
        "job_role": "Software Engineer",
        "experience_required": "Entry Level",
        "job_type": "Full-time",
        "work_mode": "On-site",
        "location": "Bangalore, India",
        "description": (
            "Build and scale backend services powering our enterprise productivity "
            "platform. You'll work across the stack with a focus on reliable, "
            "well-tested services."
        ),
        "required_skills": [
            "Data Structures & Algorithms",
            "System Design",
            "SQL",
            "Java",
            "Distributed Systems",
        ],
    },
    {
        "company_name": "Nexora Technologies",
        "job_title": "SDE Intern",
        "job_role": "SDE Intern",
        "experience_required": "Entry Level",
        "job_type": "Internship",
        "work_mode": "On-site",
        "location": "Bangalore, India",
        "description": (
            "A hands-on internship building real features alongside our engineering "
            "team, with mentorship and a path to a full-time offer."
        ),
        "required_skills": ["Data Structures & Algorithms", "Python"],
    },
    {
        "company_name": "BluePeak Software",
        "job_title": "Frontend Developer",
        "job_role": "Frontend Developer",
        "experience_required": "Entry Level",
        "job_type": "Full-time",
        "work_mode": "Hybrid",
        "location": "Pune, India",
        "description": (
            "Own user-facing features for our workflow automation product, working "
            "closely with design to ship polished, accessible interfaces."
        ),
        "required_skills": ["JavaScript", "React", "CSS"],
    },
    {
        "company_name": "Vertex Analytics",
        "job_title": "Data Analyst",
        "job_role": "Data Analyst",
        "experience_required": "Entry Level",
        "job_type": "Full-time",
        "work_mode": "Remote",
        "location": "Remote",
        "description": (
            "Turn raw operational data into decisions — build dashboards, run "
            "analyses, and partner with product teams on data-driven questions."
        ),
        "required_skills": ["SQL", "Data Analysis", "Python"],
    },
    {
        "company_name": "CloudArc Systems",
        "job_title": "Backend Developer",
        "job_role": "Backend Developer",
        "experience_required": "Mid Level",
        "job_type": "Full-time",
        "work_mode": "On-site",
        "location": "Hyderabad, India",
        "description": (
            "Design and operate the services behind our cloud infrastructure "
            "platform, with a strong emphasis on reliability and observability."
        ),
        "required_skills": ["Java", "System Design", "AWS", "SQL"],
    },
    {
        "company_name": "Quantify Labs",
        "job_title": "Machine Learning Engineer",
        "job_role": "ML Engineer",
        "experience_required": "Mid Level",
        "job_type": "Full-time",
        "work_mode": "Hybrid",
        "location": "Bangalore, India",
        "description": (
            "Build and deploy ML models that power our product's recommendation "
            "and forecasting features, from experimentation through production."
        ),
        "required_skills": ["Python", "Machine Learning", "SQL"],
    },
    {
        "company_name": "Ironclad Security",
        "job_title": "Security Engineer",
        "job_role": "Security Engineer",
        "experience_required": "Mid Level",
        "job_type": "Full-time",
        "work_mode": "On-site",
        "location": "Noida, India",
        "description": (
            "Harden our platform against real-world threats — from secure code "
            "review to incident response and security tooling."
        ),
        "required_skills": ["Networking", "Security", "Python"],
    },
    {
        "company_name": "Skyline Mobility",
        "job_title": "Mobile App Developer",
        "job_role": "Mobile App Developer",
        "experience_required": "Entry Level",
        "job_type": "Full-time",
        "work_mode": "On-site",
        "location": "Pune, India",
        "description": (
            "Build and ship features for our rider-facing mobile app used by "
            "millions of commuters every day."
        ),
        "required_skills": ["JavaScript", "React", "Mobile Development"],
    },
    {
        "company_name": "Orbit Robotics",
        "job_title": "Embedded Software Engineer",
        "job_role": "Embedded Software Engineer",
        "experience_required": "Mid Level",
        "job_type": "Full-time",
        "work_mode": "On-site",
        "location": "Chennai, India",
        "description": (
            "Write firmware and low-level control software for our robotics "
            "platform, working closely with hardware engineers."
        ),
        "required_skills": ["C++", "Embedded Systems", "Networking"],
    },
    {
        "company_name": "Northwind Retail Tech",
        "job_title": "Full Stack Developer",
        "job_role": "Full Stack Developer",
        "experience_required": "Entry Level",
        "job_type": "Part-time",
        "work_mode": "Remote",
        "location": "Remote",
        "description": (
            "Contribute across our retail platform's stack — from customer-facing "
            "storefronts to the internal tools our merchants rely on."
        ),
        "required_skills": ["JavaScript", "React", "SQL", "Java"],
    },
]


def seed_jobs(db: Session) -> None:
    if db.scalar(select(Job.id).limit(1)) is not None:
        return
    recruiter = db.scalar(select(Recruiter).where(Recruiter.mobile_number == DEMO_RECRUITER_MOBILE))
    if recruiter is None:
        return
    for entry in _JOBS:
        db.add(
            Job(
                recruiter_id=recruiter.id,
                company_name=entry["company_name"],
                job_title=entry["job_title"],
                job_role=entry["job_role"],
                experience_required=entry["experience_required"],
                job_type=entry["job_type"],
                work_mode=entry["work_mode"],
                location=entry["location"],
                description=entry["description"],
                required_skills=entry["required_skills"],
            )
        )
    db.commit()
