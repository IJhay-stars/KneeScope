<!-- KS-DATA-08 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-08: Create patient/study-grouped train, validation and test splits with leakage checks

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing with Evaluation reviewer |
| Status (from state.json) | blocked |

## Problem

Slices from one study, or studies from one patient, must never cross partitions. Validation (used for choices and thresholds) and an untouched test partition must be separate where sample size permits.

## Expected outcome

A committed split definition (artifacts are IDs only if permitted; otherwise a deterministic split script + seed + hash) assigning each study to train/validation/test, grouped by patient where identifiers exist, stratified by the selected findings where feasible; tests prove no group crosses partitions.

## Dependencies

- Blocked by: `KS-DATA-03` — Audit the accessible dataset(s): studies, series, planes, labels and grouping identifiers
- Blocked by: `KS-DATA-04` — Decide the dataset and supported finding profile
- Blocked by: `KS-LABEL-01` — Build the labels file with provenance and explicit unknown handling

- Blocks: `KS-DATA-09` — Preprocessed tensor cache and training/evaluation data loaders
- Blocks: `KS-DATA-10` — Select permitted demo studies and build the study manifest
- Blocks: `KS-MODEL-03` — Train the baseline model on the selected dataset
- Blocks: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot

## Scope

- scripts/make_splits.py with seed, grouping key and stratification.
- Leakage test: no study_id or patient group in more than one partition.
- Per-partition per-finding positive/negative/unknown counts written to docs/data-audit.md.
- If the labelled pool is too small for a test partition, record 'validation only' and the consequence for wording.

## Explicit exclusions

- No tuning on the test partition, ever.

## Implementation guidance

If patient IDs are unavailable, group by study and state this limitation in the model card. Unknown labels stay unknown in every partition.

## Relevant files and modules

- `scripts/make_splits.py`
- `tests/ml/test_splits.py`
- `docs/data-audit.md`

## Contract impact

Defines the 'partition' values used in MetricsSnapshot. No schema change.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset labelled pool.
- **Evaluation partition:** Defines train / validation / (test if feasible).
- **Applicable metrics:** Counts and prevalence per partition.
- **What cannot be claimed:** Patient-level independence if only study IDs exist; cross-site generalisation.
- **Reproducibility artifacts:** Split script, seed, split hash, counts table.

## Acceptance criteria

- [ ] scripts/make_splits.py is deterministic: two runs with the same seed produce identical split hashes.
- [ ] tests/ml/test_splits.py fails if any study or patient group appears in two partitions (tested with a deliberately leaky input).
- [ ] Per-partition counts table present; every retained finding has ≥1 positive and ≥1 negative in validation (else recorded as undefined).
- [ ] Test partition existence decision recorded.

## Verification

- `python scripts/make_splits.py --seed 2026 && python scripts/make_splits.py --seed 2026 --check-hash`
- `pytest tests/ml/test_splits.py`

## Documentation updates

- docs/data-audit.md §5
- docs/decisions.md

## Definition of done

- Evaluation owner signed off on partition sizes.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
