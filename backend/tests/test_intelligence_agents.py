"""Tests for the Student Intelligence multi-agent system (phase.md Phase
06), exercised directly through the "AI services" bridge with plain-dict
fixtures — no backend DB involved, matching how those agents are meant to
be usable standalone.
"""

import shutil
import tempfile

import pytest

from backend.core.ai_bridge import ensure_ai_services_importable

ensure_ai_services_importable()

from agents.company_intelligence_agent import CompanyIntelligenceAgent  # noqa: E402
from agents.placement_readiness_agent import PlacementReadinessAgent  # noqa: E402
from agents.preparation_plan_agent import PreparationPlanAgent  # noqa: E402
from agents.skill_gap_analysis_agent import SkillGapAnalysisAgent  # noqa: E402
from agents.student_skill_analysis_agent import StudentSkillAnalysisAgent  # noqa: E402
from agents.what_if_analysis_agent import WhatIfAnalysisAgent  # noqa: E402
from multi_agent.student_placement_intelligence import (  # noqa: E402
    run_student_intelligence_pipeline,
    run_what_if,
)
from qdrant_client import QdrantClient  # noqa: E402
from rag.ingest import ingest_companies  # noqa: E402
from rag.vector_store import ensure_collections  # noqa: E402

COMPANY = {
    "company_id": 1,
    "company_name": "Nexora Technologies",
    "industry": "Enterprise Software",
    "role_requirements": [
        {
            "role_title": "Software Engineer",
            "required_skills": [
                {"skill": "Python", "min_proficiency": "Advanced"},
                {"skill": "SQL", "min_proficiency": "Intermediate"},
                {"skill": "System Design", "min_proficiency": "Intermediate"},
            ],
            "experience_expectation": "0-2 years",
            "evidence_expectations": ["GitHub repository"],
            "project_expectations": ["Backend service"],
        }
    ],
    "patterns": ["Consistently weights DSA heavily."],
    "historical_requirements": [],
    "successful_candidate_profiles": [
        {"role_title": "Software Engineer", "profile_summary": {"typical_cgpa": 8.0}}
    ],
}


def strong_student():
    return {
        "student_id": 1,
        "skills": [
            {
                "skill_name": "Python",
                "skill_category": "Language",
                "proficiency": "Advanced",
                "learning_status": "Confident",
                "experience_years": 2,
                "evidence_count": 1,
            },
            {
                "skill_name": "SQL",
                "skill_category": "Database",
                "proficiency": "Advanced",
                "learning_status": "Confident",
                "experience_years": 1,
                "evidence_count": 0,
            },
        ],
        "projects": [
            {
                "project_name": "API Service",
                "technologies_used": ["Python"],
                "skills_demonstrated": [],
            }
        ],
        "certifications": [],
        "coding_experience": [],
        "academic": {
            "college": "Test College",
            "degree": "B.Tech",
            "branch": "CSE",
            "current_year": "3rd Year",
            "current_cgpa": 8.2,
        },
    }


def weak_student():
    return {
        "student_id": 2,
        "skills": [
            {
                "skill_name": "Python",
                "skill_category": "Language",
                "proficiency": "Beginner",
                "learning_status": "Learning",
                "experience_years": 0,
                "evidence_count": 0,
            }
        ],
        "projects": [],
        "certifications": [],
        "coding_experience": [],
        "academic": {
            "college": "Test College",
            "degree": "B.Tech",
            "branch": "CSE",
            "current_year": "1st Year",
            "current_cgpa": 7.0,
        },
    }


@pytest.fixture(scope="module")
def qdrant_with_company():
    tmp_dir = tempfile.mkdtemp()
    client = QdrantClient(path=tmp_dir)
    ensure_collections(client)
    ingest_companies(client, [COMPANY])
    yield client
    client.close()
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_company_intelligence_agent_matches_role_and_retrieves_context(qdrant_with_company):
    result = CompanyIntelligenceAgent().run(qdrant_with_company, COMPANY, "Software Engineer")
    assert result["role_matched_exactly"] is True
    assert {s["skill"] for s in result["required_skills"]} == {"Python", "SQL", "System Design"}
    assert len(result["retrieved_context"]) > 0


def test_company_intelligence_agent_falls_back_when_role_unmatched(qdrant_with_company):
    result = CompanyIntelligenceAgent().run(qdrant_with_company, COMPANY, "Data Scientist")
    assert result["role_matched_exactly"] is False
    assert result["target_role"] == "Software Engineer"  # fell back to the only defined role


def test_student_skill_analysis_agent_flags_missing_evidence():
    analysis = StudentSkillAnalysisAgent().run(strong_student())
    assert "SQL" in analysis["skills_without_evidence"]
    assert "Python" not in analysis["skills_without_evidence"]
    assert analysis["project_count"] == 1


def test_placement_readiness_full_match():
    required_skills_intel = {
        "required_skills": COMPANY["role_requirements"][0]["required_skills"],
        "target_role": "Software Engineer",
        "company_name": "Nexora Technologies",
    }
    student_analysis = StudentSkillAnalysisAgent().run(strong_student())
    readiness = PlacementReadinessAgent().run(required_skills_intel, student_analysis)
    # Python & SQL matched exactly; System Design missing -> 2/3 matched
    assert readiness["readiness_percentage"] == 67
    assert readiness["status_message"] == "Making progress — a few key gaps remain."
    assert "Python" in readiness["matched_skills"]
    assert "System Design" in readiness["unmatched_skills"]


def test_placement_readiness_no_target_returns_zero():
    readiness = PlacementReadinessAgent().run(
        {"required_skills": []}, StudentSkillAnalysisAgent().run(strong_student())
    )
    assert readiness["readiness_percentage"] == 0


def test_skill_gap_agent_categorizes_correctly():
    company_intel = {
        "company_name": "Nexora Technologies",
        "target_role": "Software Engineer",
        "required_skills": COMPANY["role_requirements"][0]["required_skills"],
    }
    student_analysis = StudentSkillAnalysisAgent().run(strong_student())
    readiness = PlacementReadinessAgent().run(company_intel, student_analysis)
    gap = SkillGapAnalysisAgent().run(company_intel, student_analysis, readiness)

    assert "Python" in gap["existing_skills"]
    assert "SQL" in gap["missing_evidence"]  # matched but evidence_count == 0
    assert "System Design" in gap["missing_skills"]
    assert gap["reasoning"]  # non-empty narrative produced
    assert gap["priority_areas"][0]["priority"] == "High"  # missing skills sorted first


def test_preparation_plan_reflects_academic_year():
    company_intel = {
        "company_name": "Nexora Technologies",
        "target_role": "Software Engineer",
        "required_skills": COMPANY["role_requirements"][0]["required_skills"],
    }
    student_analysis = StudentSkillAnalysisAgent().run(weak_student())
    readiness = PlacementReadinessAgent().run(company_intel, student_analysis)
    gap = SkillGapAnalysisAgent().run(company_intel, student_analysis, readiness)

    plan_year1 = PreparationPlanAgent().run(gap, "1st Year")
    plan_final = PreparationPlanAgent().run(gap, "Final Year")
    assert plan_year1["horizon_summary"] == "long-term"
    assert plan_final["horizon_summary"] == "short-term"
    assert len(plan_year1["items"]) > 0


def test_what_if_agent_identifies_required_topic():
    company_intel = {
        "company_name": "Nexora Technologies",
        "target_role": "Software Engineer",
        "required_skills": COMPANY["role_requirements"][0]["required_skills"],
    }
    student_analysis = StudentSkillAnalysisAgent().run(weak_student())
    readiness = PlacementReadinessAgent().run(company_intel, student_analysis)
    gap = SkillGapAnalysisAgent().run(company_intel, student_analysis, readiness)

    result = WhatIfAnalysisAgent().run(
        "What if I improve my System Design skills?",
        company_intel,
        student_analysis,
        readiness,
        gap,
        COMPANY["role_requirements"],
    )
    assert result["topic"] == "System Design"
    assert result["relevant_to_target"] is True
    assert result["current_readiness_percentage"] == readiness["readiness_percentage"]
    assert result["projected_readiness_percentage"] is not None


def test_what_if_agent_flags_irrelevant_topic():
    company_intel = {
        "company_name": "Nexora Technologies",
        "target_role": "Software Engineer",
        "required_skills": COMPANY["role_requirements"][0]["required_skills"],
    }
    student_analysis = StudentSkillAnalysisAgent().run(weak_student())
    readiness = PlacementReadinessAgent().run(company_intel, student_analysis)
    gap = SkillGapAnalysisAgent().run(company_intel, student_analysis, readiness)

    result = WhatIfAnalysisAgent().run(
        "What if I learn Generative AI?",
        company_intel,
        student_analysis,
        readiness,
        gap,
        COMPANY["role_requirements"],
    )
    assert result["topic"] == "generative ai"
    assert result["relevant_to_target"] is False
    # Not part of this role's requirements, so the projection should show
    # no change in readiness.
    assert result["projected_readiness_percentage"] == readiness["readiness_percentage"]


def test_full_pipeline_and_what_if_orchestration(qdrant_with_company):
    result = run_student_intelligence_pipeline(
        qdrant_with_company,
        company=COMPANY,
        student=weak_student(),
        target_role="Software Engineer",
    )
    assert set(result.keys()) >= {
        "company_intel",
        "student_analysis",
        "readiness",
        "skill_gap",
        "preparation_plan",
    }
    assert result["skill_gap"]["target_company"] == "Nexora Technologies"

    what_if = run_what_if(
        qdrant_with_company,
        company=COMPANY,
        student=weak_student(),
        target_role="Software Engineer",
        question="What if I improve SQL?",
    )
    assert what_if["topic"] == "SQL"
