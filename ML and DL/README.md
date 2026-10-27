# ML and DL

LOOP-MIND's statistical/learned-model layer, kept separate from `AI services/`
(the LangChain/agent layer) per `spec.md` §"FINAL REPOSITORY STRUCTURE".

This layer trains only on LOOP-MIND's own accumulated recruitment history —
never on manually invented or supplied datasets. The full loop:

```
Database -> Dataset Generation -> Preprocessing -> ML Training ->
Evaluation -> Validated Model (only if it earns acceptance) -> models/
```

Run the whole pipeline end to end:

```
python "ML and DL/run_training_pipeline.py"
```

| Directory | Purpose |
| --- | --- |
| `datasets/dataset_generation/` | `generate_recruitment_dataset.py` — reads the application's own database (`backend.core.database`, `backend.models.jobs`, `backend.models.student_profile`) and exports one row per job application (student, job, skills, matching score, shortlisting, recruiter decision, interview outcome, final outcome) to `datasets/raw/recruitment_history.csv`. Never fabricates an outcome — an application still in progress is exported with `final_outcome=None` and excluded from training. |
| `datasets/raw/` | The raw exported historical recruitment records (output of the above). |
| `datasets/processed/` | Cleaned, normalized, labeled training data (output of `preprocessing/`). |
| `preprocessing/dataset_preparation/` | `prepare_features.py` — missing-value handling, normalization, duplicate handling, and feature derivation (skill match ratio, AI status one-hot, etc.). `prepare()` keeps only applications with a *concluded* outcome (both success and failure) for training; `prepare_for_inference()` reuses the identical feature derivation to score an in-progress application, so training and inference never diverge. |
| `ml/training/` | `train_outcome_model.py` — trains a scikit-learn model (logistic regression or random forest) to predict recruitment outcome from matching/skill features. Refuses to train (reports `insufficient_data` instead) unless at least `MIN_SAMPLES_PER_CLASS` (10) concluded examples of *both* outcomes exist — it does not produce a meaningless model from too little history. |
| `dl/` | Deep learning, intentionally unused until recruitment history is large and complex enough to justify it over the `ml/` model above (spec.md §15). |
| `models/model_store.py` | Persists a trained model (`models/ML/recruitment_outcome_model.joblib`) plus its metadata (`models/metadata/recruitment_outcome_model.json`: training date, feature schema, sample size, metrics). Only ever called after a model has passed the evaluation gate below. |
| `evaluation/metrics/evaluate.py` | Computes accuracy/precision/recall/F1 on a held-out split and `should_accept_model()` gates acceptance: rejects a model below `MIN_ACCEPTABLE_ACCURACY` (0.6), and rejects a newly trained model that doesn't beat the currently validated one — so a previously validated model is never silently replaced by a worse one. |
| `run_training_pipeline.py` | Orchestrates all of the above, in order, against the real database. Because `"ML and DL"` contains spaces, its submodules can't use normal dotted `import` syntax — each is loaded via `importlib.util.spec_from_file_location` against its file path instead. |

ML/DL supports the AI agents — it must never silently replace a defined
agent workflow (`phase.md` §29 "Verify ML/DL boundary"). It is not applied to
every database table; only the recruitment-outcome dataset above has a
defined training schema. Additional ML/DL use cases are added only when a
specific problem justifies them (spec.md §14-15), following the same
dataset-generation -> preprocessing -> training -> evaluation shape.
