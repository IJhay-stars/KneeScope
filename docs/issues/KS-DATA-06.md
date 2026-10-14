<!-- KS-DATA-06 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-06: Handle orientation metadata, transfer syntaxes, missing series and corrupt inputs

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing |
| Status (from state.json) | blocked |

## Problem

RSNA series mix Explicit/Implicit VR, JPEG Lossless and JPEG 2000, with varying orientation and resolution; some files may be unreadable. Failures must surface as structured errors, not crashes or silently wrong images.

## Expected outcome

The adapter decodes every transfer syntax found in the audit, records laterality and orientation without mirroring, maps failures to PREPROCESSING_FAILED / INPUT_INVALID with safe messages, and a missing required plane yields 'unavailable' findings.

## Dependencies

- Blocked by: `KS-DATA-05` — Dataset adapter: study listing, plane assignment, series selection and slice ordering

- Blocks: `KS-DATA-07` — Freeze shared preprocessing v1 with visual inspection evidence
- Blocks: `KS-API-01` — Dataset-backed study catalogue and slice rendering in model mode

## Scope

- Add decoders (pylibjpeg/openjpeg or gdcm) to the ml extra and lock.
- Detect corrupt or inconsistent series (missing slices, mixed dimensions) and raise PreprocessingError with a reviewer-safe message.
- Record laterality and orientation metadata in SeriesVolume for display labels.
- Tests for each failure path.

## Explicit exclusions

- No image mirroring to a canonical side.

## Implementation guidance

Messages must not include file paths or UIDs. Mixed rows/cols within a series is an error unless a documented resample rule is chosen.

## Relevant files and modules

- `ml/kneescope_ml/adapters/`
- `ml/kneescope_ml/preprocess.py`
- `pyproject.toml`
- `uv.lock`
- `tests/ml/`

## Contract impact

May add optional orientation fields to SeriesSummary (additive, minor schema bump) — follow the contract change procedure if so.

## Acceptance criteria

- [ ] A test per transfer syntax present in the audit decodes a generated or permitted sample.
- [ ] Tests: truncated file, mixed slice dimensions, zero slices → PreprocessingError with a message containing no path.
- [ ] A study missing the required plane produces findings with status 'unavailable' and reason code INPUT_INVALID through the API test client.
- [ ] No code path flips pixel arrays (grep check in test).

## Verification

- `uv sync --extra ml && pytest tests/ml`
- `pytest tests/api -k unavailable`

## Documentation updates

- contracts/README.md §4 if orientation fields are added
- docs/data-audit.md

## Definition of done

- Audit's corrupt-file count reconciled with adapter failures.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
