<!-- KS-DATA-07 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-07: Freeze shared preprocessing v1 with visual inspection evidence

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing |
| Status (from state.json) | blocked |

## Problem

config/preprocessing.toml is a placeholder (prep-0.0.0-placeholder). Training and serving must use identical, versioned parameters chosen from the audit, and the output must be visually checked before training.

## Expected outcome

config/preprocessing.toml version 'prep-1.0.0' with status 'frozen'; parameters justified in docs/decisions.md; scripts/inspect_preprocessing.py writes a contact sheet of preprocessed planes for a sample of studies (kept local if terms forbid sharing); the same function is imported by training, evaluation, caching and the API.

## Dependencies

- Blocked by: `KS-DATA-05` — Dataset adapter: study listing, plane assignment, series selection and slice ordering
- Blocked by: `KS-DATA-06` — Handle orientation metadata, transfer syntaxes, missing series and corrupt inputs

- Blocks: `KS-DATA-09` — Preprocessed tensor cache and training/evaluation data loaders
- Blocks: `KS-DATA-10` — Select permitted demo studies and build the study manifest
- Blocks: `KS-API-02` — Live inference through shared preprocessing in POST /predictions

## Scope

- Choose num_slices, H, W, normalisation from audit statistics.
- Implement scripts/inspect_preprocessing.py.
- Add a test that training data loader and API call the same preprocess_study (import identity).
- Bump version; document cache invalidation.

## Explicit exclusions

- Data augmentation (belongs to training, applied after preprocessing).

## Implementation guidance

Any later change bumps the version and invalidates tensor and prediction caches (keys include the version). Keep resizing aspect-preserving.

## Relevant files and modules

- `config/preprocessing.toml`
- `ml/kneescope_ml/preprocess.py`
- `scripts/inspect_preprocessing.py`
- `tests/ml/test_preprocess.py`

## Contract impact

contracts/README.md §4 values updated; preprocessing version changes in all responses. Notify modelling, evaluation and backend owners.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset, labelled subset sample.
- **Evaluation partition:** Training partition only for any statistic used to set parameters.
- **Applicable metrics:** Not applicable.
- **What cannot be claimed:** That brightness on rendered PNGs is MRI window/level.
- **Reproducibility artifacts:** Frozen config with SHA-256, inspection script, local contact sheets.

## Acceptance criteria

- [ ] config/preprocessing.toml has version 'prep-1.0.0' and status 'frozen'.
- [ ] tests/ml/test_preprocess.py covers: output dtype float32, shape (S,H,W) per plane, mask/padding, missing plane, constant series, no slice repeats, source_slice_index mapping.
- [ ] A test asserts the training loader and API prediction path reference kneescope_ml.preprocess.preprocess_study (no second implementation).
- [ ] Contact sheets for ≥10 studies across all planes inspected; findings recorded in the PR.

## Verification

- `pytest tests/ml/test_preprocess.py`
- `python scripts/inspect_preprocessing.py --n 10 --out artifacts/inspect/`

## Documentation updates

- contracts/README.md §4
- docs/decisions.md
- docs/architecture.md

## Definition of done

- Consumers acknowledged the frozen version in the PR.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
