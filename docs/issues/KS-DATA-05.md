<!-- KS-DATA-05 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-05: Dataset adapter: study listing, plane assignment, series selection and slice ordering

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing |
| Status (from state.json) | blocked |

## Problem

Model input and the viewer need a deterministic mapping from the selected dataset to SeriesVolume objects: which series belong to which plane, which one series per plane feeds the model, and slice order by spatial position rather than filename.

## Expected outcome

ml/kneescope_ml/adapters/<dataset>.py implements DatasetAdapter (list_studies, list_series, load_series, select_series) with slice_order 'patient_position' derived from ImagePositionPatient projected on the slice normal, and a documented series-selection rule.

## Dependencies

- Blocked by: `KS-DATA-04` — Decide the dataset and supported finding profile

- Blocks: `KS-DATA-06` — Handle orientation metadata, transfer syntaxes, missing series and corrupt inputs
- Blocks: `KS-DATA-07` — Freeze shared preprocessing v1 with visual inspection evidence
- Blocks: `KS-API-01` — Dataset-backed study catalogue and slice rendering in model mode

## Scope

- Implement the adapter for the selected dataset.
- Plane from dataset metadata (RSNA Anatomical_Plane) cross-checked with ImageOrientationPatient; disagreement → warning and plane=None.
- Series selection rule per plane (e.g. prefer fluid-sensitive, fat-suppressed; tie-break by slice count) documented in docstring and data-audit.md.
- Rescale slope/intercept applied; no flipping.

## Explicit exclusions

- Corrupt-file and transfer-syntax robustness (KS-DATA-06).
- Normalisation and resizing (preprocess module).

## Implementation guidance

Never sort by filename or SOPInstanceUID. Use InstanceNumber only as a fallback with slice_order='instance_number' and a warning. Keep the adapter free of label access.

## Relevant files and modules

- `ml/kneescope_ml/adapters/`
- `tests/ml/test_adapter_<dataset>.py`
- `docs/data-audit.md`

## Contract impact

Produces SeriesVolume per contracts/README.md §2–§3. No schema change.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset (KS-DATA-04).
- **Evaluation partition:** Not applicable.
- **Applicable metrics:** Not applicable.
- **What cannot be claimed:** That planes are spatially registered to each other.
- **Reproducibility artifacts:** Adapter tests with synthetic DICOM generation.

## Acceptance criteria

- [ ] Unit tests on synthetic DICOMs (generated in the test with pydicom) prove ordering by position when filenames and InstanceNumber are shuffled.
- [ ] Test proves a plane mismatch yields plane=None and a warning.
- [ ] select_series returns at most one series per plane and follows the documented rule on a fixture with two sagittal series.
- [ ] Adapter module has no import of kneescope_ml.labels (enforced by tests/test_label_isolation.py).

## Verification

- `pytest tests/ml -k adapter`
- `pytest tests/test_label_isolation.py`

## Documentation updates

- docs/data-audit.md (series selection rule)
- docs/architecture.md (adapter section, if changed)

## Definition of done

- Visual spot check of 5 studies' ordered slices recorded in the PR (screenshots kept local if data terms forbid sharing).
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
