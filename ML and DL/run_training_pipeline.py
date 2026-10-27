"""ML/DL Training Architecture SDD — the full circular loop, wired
together and runnable end to end:

    Database -> Historical Recruitment Data -> Dataset Generation ->
    Preprocessing -> ML Training -> Evaluation -> Validated Model
    (only if it earns acceptance) -> models/

Run:
    python "ML and DL/run_training_pipeline.py"

Every stage here is genuinely functional against LOOP-MIND's real
database — this is not a placeholder. With the small amount of
recruitment history a fresh/demo deployment has, the expected and
*correct* result is "insufficient_data": the pipeline runs completely,
reports exactly how much labeled history exists, and does not train a
meaningless model just to produce one. As real recruitment outcomes
accumulate (§7-8: both successful and unsuccessful ones), re-running
this script is how the model improves — no manually supplied dataset is
ever required.

The directory name "ML and DL" contains spaces, so its subpackages can't
be imported with normal dotted `import` syntax — every submodule loads
its sibling modules via `importlib.util` against the file path instead,
the same way this script loads all of them.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _load(module_name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    generate = _load(
        "generate_recruitment_dataset",
        "datasets/dataset_generation/generate_recruitment_dataset.py",
    )
    prepare = _load("prepare_features", "preprocessing/dataset_preparation/prepare_features.py")
    train_mod = _load("train_outcome_model", "ml/training/train_outcome_model.py")
    evaluate_mod = _load("evaluate", "evaluation/metrics/evaluate.py")
    store = _load("model_store", "models/model_store.py")

    print("1/5 Generating raw dataset from the database...")
    raw_df = generate.generate_dataset()
    generate.RAW_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_df.to_csv(generate.RAW_DATASET_PATH, index=False)
    print(f"    {len(raw_df)} application records exported.")

    print("2/5 Preprocessing + labeling concluded outcomes...")
    features_df = prepare.prepare(raw_df)
    prepare.PROCESSED_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    features_df.to_csv(prepare.PROCESSED_DATASET_PATH, index=False)
    print(f"    {len(features_df)} labeled (concluded-outcome) records available for training.")

    print("3/5 Training the recruitment outcome model...")
    result = train_mod.train(features_df, prepare.FEATURE_COLUMNS, prepare.LABEL_COLUMN)
    if result.status == "insufficient_data":
        print(
            "    Not enough concluded recruitment history yet to train a meaningful model "
            f"(have {result.class_counts}, need at least {train_mod.MIN_SAMPLES_PER_CLASS} "
            "per class). No model was trained or replaced — this is the expected, correct "
            "outcome until more recruitment outcomes accumulate."
        )
        return

    print(f"    Trained on {result.sample_count} records ({result.class_counts}).")

    print("4/5 Evaluating the newly trained model...")
    report = evaluate_mod.evaluate(result.model, result.X_test, result.y_test)
    print(
        f"    accuracy={report.accuracy:.2f} precision={report.precision:.2f} "
        f"recall={report.recall:.2f} f1={report.f1:.2f}"
    )

    previous_metadata = store.load_current_metadata()
    previous_report = (
        evaluate_mod.EvaluationReport(**previous_metadata["metrics"]) if previous_metadata else None
    )
    accepted, reason = evaluate_mod.should_accept_model(report, previous_report)
    print(f"5/5 {reason}")

    if accepted:
        store.save_model(
            result.model, result.feature_columns, report, result.sample_count, result.class_counts
        )
        print(f"    Validated model saved to {store.OUTCOME_MODEL_PATH}")
    else:
        print("    Previously validated model (if any) remains in place, unchanged.")


if __name__ == "__main__":
    main()
