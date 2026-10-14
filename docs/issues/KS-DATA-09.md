<!-- KS-DATA-09 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-09: Preprocessed tensor cache and training/evaluation data loaders

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing |
| Status (from state.json) | blocked |

## Problem

Decoding DICOM every epoch is too slow for the available compute. Training and evaluation need cached tensors keyed by preprocessing version, plus loaders that yield masks and masked labels.

## Expected outcome

scripts/cache_tensors.py writes per-study .npz under artifacts/cache/<prep_version>/ (untracked); kneescope_ml.data provides a Dataset yielding PreprocessedStudy tensors, plane masks, and label vectors with a separate known-label mask.

## Dependencies

- Blocked by: `KS-DATA-07` — Freeze shared preprocessing v1 with visual inspection evidence
- Blocked by: `KS-DATA-08` — Create patient/study-grouped train, validation and test splits with leakage checks

- Blocks: `KS-MODEL-01` — Simple comparator baseline for every selected finding
- Blocks: `KS-MODEL-03` — Train the baseline model on the selected dataset

## Scope

- Cache writer with resume and integrity check (shape, dtype, version).
- PyTorch Dataset/DataLoader for a split.
- Label vector + mask from KS-LABEL-01 output (unknown → mask 0).
- Throughput measurement recorded.

## Explicit exclusions

- Augmentation policy beyond simple, documented options.

## Implementation guidance

Cache key = study_id + preprocessing version + config SHA. A stale cache must be detected, not silently used.

## Relevant files and modules

- `scripts/cache_tensors.py`
- `ml/kneescope_ml/data.py`
- `tests/ml/test_data.py`

## Contract impact

None (internal), but must honour contracts/README.md §4.

## Acceptance criteria

- [ ] Loading a cache entry written with a different preprocessing version raises an error (test).
- [ ] Dataset yields tensors of contract shape and a label mask where unknown labels are 0 (test with fixture labels).
- [ ] Cache build for the training subset completes and reports studies/second in the PR.

## Verification

- `pytest tests/ml/test_data.py`
- `python scripts/cache_tensors.py --split train --limit 20`

## Documentation updates

- docs/architecture.md (data flow)

## Definition of done

- Cache location and size documented in README 'Data' section.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
