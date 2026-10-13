<!-- KS-LABEL-01 | generated from docs/issues/src/03-labels.toml by scripts/backlog.py; edit the source, not this file -->
# KS-LABEL-01: Build the labels file with provenance and explicit unknown handling

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-LABELS` |
| Workstream | labels |
| Recommended owner role | Labels/explainability |
| Status (from state.json) | blocked |

## Problem

Training, splitting, evaluation and the 'Reveal dataset label' view need one labels table per selected finding with states positive/negative/unknown/not_labeled and provenance. Missing or uncertain labels must not become negatives.

## Expected outcome

scripts/build_labels.py produces artifacts/labels/<dataset>.parquet (or CSV) with study_id, finding_id, state, provenance, source_ref; kneescope_ml.labels loads it; counts match the audit.

## Dependencies

- Blocked by: `KS-DATA-04` — Decide the dataset and supported finding profile

- Blocks: `KS-DATA-08` — Create patient/study-grouped train, validation and test splits with leakage checks
- Blocks: `KS-LABEL-02` — [Conditional] Extract labels from radiology reports with negation, uncertainty and provenance
- Blocks: `KS-MODEL-01` — Simple comparator baseline for every selected finding
- Blocks: `KS-MODEL-03` — Train the baseline model on the selected dataset
- Blocks: `KS-EVAL-06` — Complete the model card from evaluated evidence
- Blocks: `KS-API-05` — Serve real labels, metrics snapshot and model card

## Scope

- Map dataset columns to finding IDs via contracts/findings.json dataset_columns.
- States: dataset 1 → positive, 0 → negative, blank/uncertain → unknown, study outside labelled subset → not_labeled.
- Provenance: expert_annotation or dataset_provided as documented by the dataset.
- Loader returns DatasetLabel records for the API.

## Explicit exclusions

- Report-derived labels (KS-LABEL-02, conditional).
- Any import from the inference path.

## Implementation guidance

Keep labels out of git if terms restrict them. The loader lives in kneescope_ml.labels, which the isolation test forbids in inference/preprocess modules.

## Relevant files and modules

- `scripts/build_labels.py`
- `ml/kneescope_ml/labels.py`
- `tests/ml/test_labels.py`

## Contract impact

Feeds StudyLabels (contracts §8). No schema change.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset's provided labels (RSNA: labelled subset of train.csv).
- **Evaluation partition:** All labelled studies (split assignment happens in KS-DATA-08).
- **Applicable metrics:** Counts per state.
- **What cannot be claimed:** That unknown labels are negative; that labels are clinical ground truth beyond the dataset's annotation process.
- **Reproducibility artifacts:** Labels file (untracked if restricted), build script, count check.

## Acceptance criteria

- [ ] Per-finding counts from the labels file equal the KS-DATA-03 audit counts (test or script check).
- [ ] A test proves blank/uncertain values become 'unknown', never 'negative'.
- [ ] tests/test_label_isolation.py still passes.

## Verification

- `python scripts/build_labels.py --dataset <id> --check-against artifacts/audit/<id>.json`
- `pytest tests/ml/test_labels.py tests/test_label_isolation.py`

## Documentation updates

- docs/data-audit.md §3 'Labels'
- docs/model-card.md (labels section)

## Definition of done

- Label provenance stated per finding in the model card draft.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
