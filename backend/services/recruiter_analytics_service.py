"""Recruiter Analytics & Historical Intelligence aggregation — phase.md
Phase 17.

Every number here is a genuine aggregate over this recruiter's own stored
`Job`/`JobApplication`/`AIMatchResult`/`HumanApproval`/`Interview` rows —
spec.md's "Dynamic rule": "All statistics and charts derive from stored
project data. No permanent screenshot values." `_weekly_application_counts`
is the one place pandas does real work (a time-series resample over actual
`applied_at` timestamps) — spec.md's own data-processing stack
(pandas + NumPy) used honestly rather than for decoration; a full
scikit-learn model is skipped because this build's realistic dataset sizes
are far too small to fit one without fabricating sophistication the data
doesn't support.
"""

from collections import Counter

import pandas as pd
from sqlalchemy.orm import Session

from backend.models.jobs import JobApplication
from backend.schemas.recruiter_analytics import (
    CompanyPatternOut,
    FunnelStageOut,
    OutcomeSliceOut,
    RecruiterAnalyticsOut,
    SkillTrendOut,
    StageTrendPointOut,
    SuccessfulCandidateProfileOut,
)
from backend.services.application_status import bucket, recruiter_applications

_TOP_SKILLS_LIMIT = 8
_STAGE_TREND_WEEKS = 8


def _funnel(applications: list[JobApplication]) -> list[FunnelStageOut]:
    applied = len(applications)
    ai_shortlisted = sum(
        1 for a in applications if a.match_result and a.match_result.ai_status == "shortlisted"
    )
    approved = sum(1 for a in applications if a.approval and a.approval.decision == "approved")
    interviewed = sum(
        1 for a in applications if a.interview and a.interview.status in ("scheduled", "completed")
    )
    hired = sum(1 for a in applications if a.interview and a.interview.outcome == "hired")
    return [
        FunnelStageOut(label="Applied", count=applied),
        FunnelStageOut(label="AI Shortlisted", count=ai_shortlisted),
        FunnelStageOut(label="Approved", count=approved),
        FunnelStageOut(label="Interviewed", count=interviewed),
        FunnelStageOut(label="Hired", count=hired),
    ]


def _outcomes(applications: list[JobApplication]) -> list[OutcomeSliceOut]:
    counts: Counter[str] = Counter()
    for application in applications:
        interview = application.interview
        if interview and interview.outcome == "hired":
            counts["Hired"] += 1
        elif interview and interview.outcome == "not_selected":
            counts["Not Selected"] += 1
        elif application.approval and application.approval.decision == "disapproved":
            counts["Disapproved"] += 1
        elif bucket(application) == "shortlisted":
            counts["Shortlisted (Pending)"] += 1
        else:
            counts["Under Review"] += 1
    return [OutcomeSliceOut(label=label, count=count) for label, count in counts.items()]


def _skill_trends(applications: list[JobApplication]) -> list[SkillTrendOut]:
    counts: Counter[str] = Counter()
    for application in applications:
        if application.match_result and application.match_result.matching_factors:
            for skill in application.match_result.matching_factors.get("matched_skills", []):
                counts[skill] += 1
    return [
        SkillTrendOut(skill=skill, count=count)
        for skill, count in counts.most_common(_TOP_SKILLS_LIMIT)
    ]


def _skill_gap_trends(applications: list[JobApplication]) -> list[SkillTrendOut]:
    counts: Counter[str] = Counter()
    for application in applications:
        if application.match_result and application.match_result.matching_factors:
            for skill in application.match_result.matching_factors.get("missing_skills", []):
                counts[skill] += 1
    return [
        SkillTrendOut(skill=skill, count=count)
        for skill, count in counts.most_common(_TOP_SKILLS_LIMIT)
    ]


def _weekly_application_counts(applications: list[JobApplication]) -> list[StageTrendPointOut]:
    if not applications:
        return []
    series = pd.Series(
        1, index=pd.to_datetime([a.applied_at for a in applications]).tz_localize(None)
    )
    weekly = series.resample("W").count()
    weekly = weekly.tail(_STAGE_TREND_WEEKS)
    return [
        StageTrendPointOut(period=period.strftime("%b %d"), applications=int(count))
        for period, count in weekly.items()
    ]


def _company_patterns(applications: list[JobApplication]) -> list[CompanyPatternOut]:
    by_job: dict[int, list[JobApplication]] = {}
    for application in applications:
        by_job.setdefault(application.job_id, []).append(application)

    patterns = []
    for job_id, job_applications in by_job.items():
        job = job_applications[0].job
        hired = sum(1 for a in job_applications if a.interview and a.interview.outcome == "hired")
        scores = [
            a.match_result.ai_score
            for a in job_applications
            if a.match_result and a.match_result.ai_score is not None
        ]
        patterns.append(
            CompanyPatternOut(
                job_id=job_id,
                job_title=job.job_title,
                job_role=job.job_role,
                applications=len(job_applications),
                hire_rate_percentage=round(hired / len(job_applications) * 100),
                average_ai_score=round(sum(scores) / len(scores)) if scores else None,
            )
        )
    return sorted(patterns, key=lambda p: p.applications, reverse=True)


def _successful_candidate_profile(
    applications: list[JobApplication],
) -> SuccessfulCandidateProfileOut:
    hired = [a for a in applications if a.interview and a.interview.outcome == "hired"]
    skill_counts: Counter[str] = Counter()
    scores = []
    for application in hired:
        if application.match_result and application.match_result.matching_factors:
            for skill in application.match_result.matching_factors.get("matched_skills", []):
                skill_counts[skill] += 1
        if application.match_result and application.match_result.ai_score is not None:
            scores.append(application.match_result.ai_score)

    return SuccessfulCandidateProfileOut(
        total_hired=len(hired),
        average_ai_score=round(sum(scores) / len(scores)) if scores else None,
        top_skills=[skill for skill, _ in skill_counts.most_common(_TOP_SKILLS_LIMIT)],
    )


def get_analytics(db: Session, recruiter_id: int) -> RecruiterAnalyticsOut:
    applications = recruiter_applications(db, recruiter_id)
    return RecruiterAnalyticsOut(
        funnel=_funnel(applications),
        outcomes=_outcomes(applications),
        skill_trends=_skill_trends(applications),
        skill_gap_trends=_skill_gap_trends(applications),
        stage_trends=_weekly_application_counts(applications),
        company_patterns=_company_patterns(applications),
        successful_candidate_profile=_successful_candidate_profile(applications),
    )
