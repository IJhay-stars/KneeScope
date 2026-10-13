<!-- KS-EVAL-05 | generated from docs/issues/src/05-eval.toml by scripts/backlog.py; edit the source, not this file -->
# KS-EVAL-05: [Conditional] Calibration assessment and temperature scaling

| Field | Value |
|---|---|
| Type | conditional |
| Priority | P2 |
| Epic | `KS-EPIC-EVAL` |
| Workstream | evaluation |
| Recommended owner role | Evaluation |
| Status (from state.json) | conditional-pending |

> **Trigger condition:** Triggered only if the validation partition has enough positives per finding to assess calibration (threshold recorded in docs/decisions.md, e.g. ≥50 positives and ≥50 negatives).

## Problem

Scores are uncalibrated by default. Calling them probabilities requires evidence.

## Expected outcome

Reliability diagrams and Brier score before/after temperature scaling fitted on validation; if adopted, score_kind becomes calibrated_probability only for findings that pass, and the model card says so.

## Dependencies

- Blocked by: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot

- None.

## Scope

- Fit temperature on validation.
- Assess on the final partition.
- Update ScoreKind only where justified.

## Explicit exclusions

- Isotonic regression on small samples.

## Implementation guidance

Until this passes, the UI and docs say 'model score'.

## Relevant files and modules

- `ml/kneescope_ml/calibration.py`
- `tests/ml/test_calibration.py`
- `docs/model-card.md`

## Contract impact

score_kind may change to calibrated_probability; MetricsSnapshot.calibration='assessed'.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset.
- **Evaluation partition:** Fit on validation; assess on final partition.
- **Applicable metrics:** Brier score, reliability bins.
- **What cannot be claimed:** Calibration on other sites or datasets.
- **Reproducibility artifacts:** Temperature values, reliability data.

## Acceptance criteria

- [ ] Sample-size threshold recorded before fitting.
- [ ] Reliability diagram data and Brier scores per finding saved.
- [ ] Test: temperature scaling never changes ranking (AUC identical before/after).

## Verification

- `pytest tests/ml/test_calibration.py`

## Documentation updates

- docs/model-card.md
- docs/decisions.md

## Definition of done

- UI wording verified for calibrated vs uncalibrated.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
