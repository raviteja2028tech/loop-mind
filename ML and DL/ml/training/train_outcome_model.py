"""ML/DL Training Architecture SDD §3: the ML layer's one currently-
justified task — predicting recruitment outcome (success/failure) from a
candidate/job's actual matching data. A statistical prediction is
justified here because there's a genuine historical-pattern question
("which candidate/job feature combinations tend to end in a hire?") and
a real (if currently small) labeled dataset to learn it from — spec.md's
own "if a deterministic calculation is sufficient, use a deterministic
calculation... if statistical prediction is justified by sufficient
historical data, use ML" principle.

Deliberately conservative: below `MIN_SAMPLES_PER_CLASS` labeled examples
per class, `train()` refuses to fit a model at all and reports
"insufficient_data" rather than producing an overfit, meaningless one —
matching the SDD's explicit permission for a training stage to stay
unused until enough suitable history has accumulated.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

MIN_SAMPLES_PER_CLASS = 10


@dataclass
class TrainingResult:
    status: str  # "trained" | "insufficient_data"
    model: object | None
    feature_columns: list[str]
    sample_count: int
    class_counts: dict[str, int]
    X_test: pd.DataFrame | None = None
    y_test: pd.Series | None = None


def _class_counts(y: pd.Series) -> dict[str, int]:
    return {"success": int((y == 1).sum()), "failure": int((y == 0).sum())}


def train(
    features_df: pd.DataFrame,
    feature_columns: list[str],
    label_column: str,
    model_type: str = "logistic_regression",
) -> TrainingResult:
    """`features_df` must already be the labeled, feature-ready dataset
    `preprocessing/dataset_preparation/prepare_features.py::prepare`
    produces. Never trains on a single-class dataset (a model that only
    ever saw one outcome is meaningless) or too few examples of either
    class."""
    counts = _class_counts(features_df[label_column])
    sample_count = len(features_df)

    if counts["success"] < MIN_SAMPLES_PER_CLASS or counts["failure"] < MIN_SAMPLES_PER_CLASS:
        return TrainingResult(
            status="insufficient_data",
            model=None,
            feature_columns=feature_columns,
            sample_count=sample_count,
            class_counts=counts,
        )

    X = features_df[feature_columns]
    y = features_df[label_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    if model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
    else:
        model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return TrainingResult(
        status="trained",
        model=model,
        feature_columns=feature_columns,
        sample_count=sample_count,
        class_counts=counts,
        X_test=X_test,
        y_test=y_test,
    )
