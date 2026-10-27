"""ML/DL Training Architecture SDD §5: stores trained model artifacts and
their metadata — never overwrites a previously validated model with a
newly trained one that hasn't passed `evaluation/metrics/evaluate.py`'s
acceptance gate first.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import joblib

ML_MODELS_DIR = Path(__file__).resolve().parent / "ML"
METADATA_DIR = Path(__file__).resolve().parent / "metadata"

OUTCOME_MODEL_PATH = ML_MODELS_DIR / "recruitment_outcome_model.joblib"
OUTCOME_METADATA_PATH = METADATA_DIR / "recruitment_outcome_model.json"


def load_current_metadata() -> dict | None:
    if not OUTCOME_METADATA_PATH.exists():
        return None
    return json.loads(OUTCOME_METADATA_PATH.read_text())


def load_current_model():
    if not OUTCOME_MODEL_PATH.exists():
        return None
    return joblib.load(OUTCOME_MODEL_PATH)


def save_model(
    model, feature_columns: list[str], report, sample_count: int, class_counts: dict
) -> dict:
    """Persists the model artifact plus its metadata (training date,
    feature schema, sample size, evaluation metrics) — the metadata is
    what a future run compares a new candidate model against via
    `evaluation.metrics.evaluate.should_accept_model`."""
    ML_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, OUTCOME_MODEL_PATH)
    metadata = {
        "trained_at": datetime.now(UTC).isoformat(),
        "feature_columns": feature_columns,
        "sample_count": sample_count,
        "class_counts": class_counts,
        "metrics": asdict(report),
    }
    OUTCOME_METADATA_PATH.write_text(json.dumps(metadata, indent=2))
    return metadata
