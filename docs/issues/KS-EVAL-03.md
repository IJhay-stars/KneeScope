<!-- KS-EVAL-03 | generated from docs/issues/src/05-eval.toml by scripts/backlog.py; edit the source, not this file -->
# KS-EVAL-03: Held-out evaluation run and published metrics snapshot

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-EVAL` |
| Workstream | evaluation |
| Recommended owner role | Evaluation |
| Status (from state.json) | blocked |

## Problem

The metrics page must show measured performance of the served checkpoint on a documented partition with sample counts, and distinguish validation results from untouched test results.

## Expected outcome

scripts/evaluate.py produces artifacts/metrics/<model_version>.json (a MetricsSnapshot) for the final partition — 'test' only if the test partition was untouched during development, otherwise 'validation' — including comparator results in the model card and inference measurements from KS-OPS-03 when available.

## Dependencies

- Blocked by: `KS-MODEL-03` — Train the baseline model on the selected dataset
- Blocked by: `KS-MODEL-01` — Simple comparator baseline for every selected finding
- Blocked by: `KS-EVAL-02` — Select per-finding operating thresholds on the validation partition
- Blocked by: `KS-DATA-08` — Create patient/study-grouped train, validation and test splits with leakage checks

- Blocks: `KS-MODEL-04` — [Conditional] One improvement round (fine-tuning or adjacent-slice input)
- Blocks: `KS-EVAL-04` — Error analysis: false positives, false negatives and failure cases
- Blocks: `KS-EVAL-05` — [Conditional] Calibration assessment and temperature scaling
- Blocks: `KS-EVAL-06` — Complete the model card from evaluated evidence
- Blocks: `KS-API-05` — Serve real labels, metrics snapshot and model card
- Blocks: `KS-OPT-06` — [Optional] Additional supported findings

## Scope

- Run the served checkpoint once on the final partition.
- Include per-finding counts, undefined AUCs, macro AUC with exclusions.
- Record split method and grouping unit.
- Copy the snapshot to the location served by GET /metrics (KS-API-05).

## Explicit exclusions

- Re-running test evaluation after changes to model or thresholds (would make it a validation result).

## Implementation guidance

If the result is weak, publish it. A useful failure analysis (KS-EVAL-04) is stronger evidence than an inflated number. Do not describe AUC as accuracy.

## Relevant files and modules

- `scripts/evaluate.py`
- `artifacts/metrics/ (decide tracked vs untracked by data terms)`
- `docs/model-card.md`

## Contract impact

Produces MetricsSnapshot served by /metrics.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset.
- **Evaluation partition:** Untouched test if available; otherwise validation, labelled as such.
- **Applicable metrics:** Per-finding ROC AUC, PR AUC, prevalence, sens/spec at validation threshold, Brier, macro AUC; latency/memory if measured.
- **What cannot be claimed:** Cross-site generalisation from single-site data; accuracy; clinical validity; calibrated probabilities.
- **Reproducibility artifacts:** Snapshot JSON with checkpoint SHA, seed, split hash, script version.

## Acceptance criteria

- [ ] Snapshot validates as MetricsSnapshot with status 'available', partition set, split_method, grouping_unit, n_studies, created_at, model.checkpoint_sha256.
- [ ] Every retained finding shows n_positive, n_negative, n_unknown.
- [ ] If partition is 'test', docs/experiments.md shows no prior test evaluation of this or earlier checkpoints.
- [ ] Comparator snapshot from KS-MODEL-01 on the same partition exists.

## Verification

- `python scripts/evaluate.py --run <run_id> --split test|validation`
- `python scripts/validate_artifact.py MetricsSnapshot artifacts/metrics/<model_version>.json`

## Documentation updates

- docs/model-card.md (evaluation)
- docs/experiments.md

## Definition of done

- Independent reviewer (QA role) re-runs the script and gets identical numbers.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
