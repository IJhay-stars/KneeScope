<!-- KS-EVAL-02 | generated from docs/issues/src/05-eval.toml by scripts/backlog.py; edit the source, not this file -->
# KS-EVAL-02: Select per-finding operating thresholds on the validation partition

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-EVAL` |
| Workstream | evaluation |
| Recommended owner role | Evaluation |
| Status (from state.json) | blocked |

## Problem

Sensitivity and specificity require a declared threshold. Choosing it on test data or after looking at test results inflates numbers.

## Expected outcome

A documented rule (e.g. maximise Youden's J, or reach a target sensitivity) applied on validation scores only, producing per-finding thresholds stored with the checkpoint metadata and exposed as FindingResult.threshold.

## Dependencies

- Blocked by: `KS-EVAL-01` — Metrics module: per-finding AUCs with undefined handling, counts, threshold metrics and macro AUC
- Blocked by: `KS-MODEL-03` — Train the baseline model on the selected dataset

- Blocks: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot
- Blocks: `KS-OPT-03` — [Optional] Exploratory threshold slider per finding

## Scope

- Declare the rule before computing.
- Store thresholds in artifacts/runs/<id>/thresholds.json and reference from config/model.toml.
- If a finding's validation set is single-class, no threshold (null).

## Explicit exclusions

- Interactive threshold slider (optional KS-OPT-03).

## Implementation guidance

Thresholds are operating points for a research display, not clinical cut-offs. The UI shows 'Above/Below threshold' only when a threshold exists.

## Relevant files and modules

- `ml/kneescope_ml/evaluation.py`
- `scripts/select_thresholds.py`
- `tests/ml/test_thresholds.py`

## Contract impact

Populates FindingResult.threshold/above_threshold and FindingMetrics.threshold_selected_on='validation'.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset.
- **Evaluation partition:** Validation only.
- **Applicable metrics:** Sensitivity, specificity at the selected threshold.
- **What cannot be claimed:** That thresholds are clinically appropriate.
- **Reproducibility artifacts:** thresholds.json with rule name and run_id.

## Acceptance criteria

- [ ] Rule recorded in docs/decisions.md before thresholds are computed (commit order visible in PR).
- [ ] Test proves the selector refuses a partition named 'test'.
- [ ] thresholds.json lists every supported finding with a value or null and a reason.

## Verification

- `pytest tests/ml/test_thresholds.py`
- `python scripts/select_thresholds.py --run <run_id> --split validation`

## Documentation updates

- docs/decisions.md
- docs/model-card.md

## Definition of done

- Thresholds referenced by served config.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
