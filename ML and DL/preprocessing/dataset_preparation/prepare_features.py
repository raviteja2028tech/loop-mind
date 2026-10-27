"""ML/DL Training Architecture SDD §2: turns the raw historical
recruitment dataset (`datasets/dataset_generation`'s output) into a
training-ready feature table.

Responsibilities, in order (§2's own diagram):
    missing-value handling -> normalization -> duplicate handling ->
    consistent representation -> processed dataset -> feature derivation

Only applications with a *concluded* `final_outcome` become labeled
training rows — an in-progress application has no ground truth yet and
including it would either have to fabricate a label or leave one blank,
neither of which this project allows (§8: "do not fabricate a
recruitment outcome"). The same feature derivation is reused for
inference so the exact features a model saw in training match what it
sees when scoring a new record (`ml/prediction` imports this module
rather than recomputing features differently).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROCESSED_DATASET_PATH = (
    Path(__file__).resolve().parents[2] / "datasets" / "processed" / "recruitment_features.csv"
)

FEATURE_COLUMNS = [
    "required_skills_count",
    "student_skills_count",
    "matched_skills_count",
    "missing_skills_count",
    "skill_match_ratio",
    "ai_score",
    "ai_status_shortlisted",
    "ai_status_hold",
    "ai_status_rejected",
    "interview_reached",
]
LABEL_COLUMN = "outcome_success"


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Missing-value handling + duplicate handling — the first two stages
    of §2's pipeline."""
    df = df.drop_duplicates(subset="application_id").copy()
    df["ai_score"] = df["ai_score"].fillna(
        df["ai_score"].median() if df["ai_score"].notna().any() else 0.0
    )
    df["ai_status"] = df["ai_status"].fillna("not_evaluated")
    df["required_skills_count"] = df["required_skills_count"].fillna(0)
    df["student_skills_count"] = df["student_skills_count"].fillna(0)
    df["matched_skills_count"] = df["matched_skills_count"].fillna(0)
    df["missing_skills_count"] = df["missing_skills_count"].fillna(0)
    return df


def derive_features(df: pd.DataFrame) -> pd.DataFrame:
    """Normalization + consistent representation + feature derivation —
    the remaining stages of §2's pipeline, producing exactly
    `FEATURE_COLUMNS`."""
    df = df.copy()
    df["skill_match_ratio"] = df.apply(
        lambda row: (
            (row["matched_skills_count"] / row["required_skills_count"])
            if row["required_skills_count"] > 0
            else 0.0
        ),
        axis=1,
    )
    for status in ("shortlisted", "hold", "rejected"):
        df[f"ai_status_{status}"] = (df["ai_status"] == status).astype(int)
    df["interview_reached"] = df["interview_reached"].astype(int)
    return df


def label_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """Keeps only applications with a concluded outcome and encodes it as
    a binary label — 1 for success (hired), 0 for failure. Both classes
    are preserved (never trained on successes alone)."""
    concluded = df[df["final_outcome"].notna()].copy()
    concluded[LABEL_COLUMN] = (concluded["final_outcome"] == "success").astype(int)
    return concluded


def prepare(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Full pipeline: raw dataset -> processed, labeled, feature-ready
    dataset. Returns only concluded (labeled) rows — the shape a training
    step needs."""
    df = clean(raw_df)
    df = derive_features(df)
    df = label_outcomes(df)
    return df[["application_id", *FEATURE_COLUMNS, LABEL_COLUMN]]


def prepare_for_inference(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Same feature derivation as training, without requiring (or
    discarding rows for) a concluded outcome — used to score an
    in-progress application."""
    df = clean(raw_df)
    df = derive_features(df)
    return df[["application_id", *FEATURE_COLUMNS]]
