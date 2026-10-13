<!-- KS-LABEL-03 | generated from docs/issues/src/03-labels.toml by scripts/backlog.py; edit the source, not this file -->
# KS-LABEL-03: Influential-slice explanations aligned to series slice coordinates

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-LABELS` |
| Workstream | labels |
| Recommended owner role | Labels/explainability |
| Status (from state.json) | blocked |

## Problem

Reviewers want to jump to the slices that most influenced a finding's score. Slice weights from the model refer to sampled tensor positions and must be mapped back to series slice_index via source_slice_index, for the same study, finding, prediction and checkpoint.

## Expected outcome

kneescope_ml.explain.influential_slices(output, preprocessed, finding_id) returns an Explanation (kind influential_slices) with series slice indices and relative weights; failures return status 'unavailable' with a reason.

## Dependencies

- Blocked by: `KS-MODEL-03` — Train the baseline model on the selected dataset

- Blocks: `KS-LABEL-04` — [Optional] Grad-CAM attention maps with alignment verification
- Blocks: `KS-API-03` — Serve real explanations with alignment validation

## Scope

- Derive per-finding slice weights (attention pooling weights or gradient-based slice importance — document which).
- Map through source_slice_index; drop padding.
- Return Explanation with series_id, plane, rendered size, prediction_id and model_version.
- Alignment test with a synthetic volume where the influential slice is known.

## Explicit exclusions

- Pixel-level heatmaps (KS-LABEL-04, optional).
- Wording that implies lesion location.

## Implementation guidance

Name it 'Influential slices'. If the model has no slice-level signal for a finding, return unavailable rather than inventing weights.

## Relevant files and modules

- `ml/kneescope_ml/explain.py`
- `tests/ml/test_explain.py`

## Contract impact

Produces Explanation (contracts §7). No schema change.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset; evaluation partition for any qualitative review.
- **Evaluation partition:** Validation or test, stated when screenshots are used.
- **Applicable metrics:** None (qualitative); alignment correctness is tested.
- **What cannot be claimed:** That influential slices localise or prove an injury.
- **Reproducibility artifacts:** Explanation code version tied to checkpoint; alignment tests.

## Acceptance criteria

- [ ] Synthetic test: a volume whose only non-zero slice is index k yields k as the top influential slice after mapping.
- [ ] Explanations for padding positions never appear (test).
- [ ] Explanation validates against the contract and carries the matching prediction_id and model_version.
- [ ] Unavailable path returns reason code EXPLANATION_UNAVAILABLE.

## Verification

- `pytest tests/ml/test_explain.py`

## Documentation updates

- docs/model-card.md (explanations section)
- contracts/README.md §7 if behaviour clarifies

## Definition of done

- Owner of KS-API-03 confirms the function signature.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
