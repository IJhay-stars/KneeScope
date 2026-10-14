<!-- KS-MODEL-01 | generated from docs/issues/src/04-model.toml by scripts/backlog.py; edit the source, not this file -->
# KS-MODEL-01: Simple comparator baseline for every selected finding

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-MODEL` |
| Workstream | modelling |
| Recommended owner role | Modelling |
| Status (from state.json) | blocked |

## Problem

A deep model's AUC means little without a reference. The plan requires comparison with a simple baseline.

## Expected outcome

A documented simple comparator (e.g. logistic regression on per-plane intensity statistics and slice counts, plus the constant-prevalence predictor) evaluated on the same validation partition with the same metrics module.

## Dependencies

- Blocked by: `KS-DATA-09` — Preprocessed tensor cache and training/evaluation data loaders
- Blocked by: `KS-LABEL-01` — Build the labels file with provenance and explicit unknown handling
- Blocked by: `KS-EVAL-01` — Metrics module: per-finding AUCs with undefined handling, counts, threshold metrics and macro AUC

- Blocks: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot

## Scope

- Implement comparator(s) in ml/kneescope_ml/baselines.py.
- Evaluate on validation with kneescope_ml.evaluation.
- Record results in the run registry.

## Explicit exclusions

- Tuning on the test partition.

## Implementation guidance

Keep it cheap. The constant predictor's ROC AUC is 0.5 by construction and only shows the metric pipeline works; the image-statistics comparator is the meaningful reference.

## Relevant files and modules

- `ml/kneescope_ml/baselines.py`
- `scripts/run_baselines.py`
- `tests/ml/test_baselines.py`

## Contract impact

None.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset, cached tensors.
- **Evaluation partition:** Validation.
- **Applicable metrics:** Per-finding ROC AUC, PR AUC, prevalence, counts.
- **What cannot be claimed:** Clinical meaning of any comparator score.
- **Reproducibility artifacts:** Run directory with config, seed, split hash, metrics JSON.

## Acceptance criteria

- [ ] scripts/run_baselines.py writes a MetricsSnapshot-shaped JSON for the comparator on the validation partition.
- [ ] Comparator results appear in the model card evaluation section next to the main model (KS-EVAL-06).
- [ ] Test runs the comparator end to end on synthetic tensors.

## Verification

- `pytest tests/ml/test_baselines.py`
- `python scripts/run_baselines.py --split validation`

## Documentation updates

- docs/model-card.md
- docs/experiments.md

## Definition of done

- Results reproducible from the recorded seed and split hash.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
