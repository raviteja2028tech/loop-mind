"""ML/DL Training Architecture SDD §6: every trained model is evaluated
before it can ever be used — a model is never assumed better just
because it's newer. `should_accept_model` is the acceptance gate:
`models/model_store.py` calls it before ever overwriting a previously
validated model's artifact.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

MIN_ACCEPTABLE_ACCURACY = 0.6


@dataclass
class EvaluationReport:
    accuracy: float
    precision: float
    recall: float
    f1: float
    sample_count: int


def evaluate(model, X_test: pd.DataFrame, y_test: pd.Series) -> EvaluationReport:
    predictions = model.predict(X_test)
    return EvaluationReport(
        accuracy=float(accuracy_score(y_test, predictions)),
        precision=float(precision_score(y_test, predictions, zero_division=0)),
        recall=float(recall_score(y_test, predictions, zero_division=0)),
        f1=float(f1_score(y_test, predictions, zero_division=0)),
        sample_count=len(y_test),
    )


def should_accept_model(
    new_report: EvaluationReport, previous_report: EvaluationReport | None
) -> tuple[bool, str]:
    """Rejects a model below `MIN_ACCEPTABLE_ACCURACY` outright, and never
    lets a newly trained model silently replace a previously validated
    one unless it's at least as good on the metric that matters most
    here (accuracy) — spec.md/§6's "must not automatically replace a
    previously validated model with an unvalidated newly trained model"."""
    if new_report.accuracy < MIN_ACCEPTABLE_ACCURACY:
        return False, (
            f"Rejected: accuracy {new_report.accuracy:.2f} is below the "
            f"minimum acceptable {MIN_ACCEPTABLE_ACCURACY:.2f}."
        )
    if previous_report is not None and new_report.accuracy < previous_report.accuracy:
        return False, (
            f"Rejected: new accuracy {new_report.accuracy:.2f} does not beat the "
            f"currently validated model's {previous_report.accuracy:.2f}."
        )
    return True, "Accepted."
