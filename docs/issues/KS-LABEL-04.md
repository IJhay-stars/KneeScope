<!-- KS-LABEL-04 | generated from docs/issues/src/03-labels.toml by scripts/backlog.py; edit the source, not this file -->
# KS-LABEL-04: [Optional] Grad-CAM attention maps with alignment verification

| Field | Value |
|---|---|
| Type | optional |
| Priority | P2 |
| Epic | `KS-EPIC-LABELS` |
| Workstream | labels |
| Recommended owner role | Labels/explainability |
| Status (from state.json) | optional-blocked |

## Problem

Pixel-level model attention can help reviewers see what influenced a score, but it is easy to misalign or over-interpret.

## Expected outcome

Optional AttentionMap entries (png_base64_gray8) at rendered slice size for the top influential slices, produced only when the alignment check passes.

## Dependencies

- Blocked by: `KS-LABEL-03` — Influential-slice explanations aligned to series slice coordinates

- None.

## Scope

- Grad-CAM on the 2D encoder for selected slices.
- Resample from tensor space back to rendered slice pixels (undo padding and resize).
- Alignment test with a synthetic marker.

## Explicit exclusions

- Rainbow/jet colour maps (UI uses single-hue ochre→rust).
- Lesion terminology.

## Implementation guidance

If the backbone or resize path makes inverse mapping ambiguous, ship influential slices only.

## Relevant files and modules

- `ml/kneescope_ml/explain.py`
- `tests/ml/test_gradcam_alignment.py`

## Contract impact

Uses AttentionMap (already in contract).

## Scientific requirements

- **Dataset and label provenance:** Selected dataset.
- **Evaluation partition:** Validation/test, stated.
- **Applicable metrics:** Alignment error in pixels on synthetic tests.
- **What cannot be claimed:** Lesion localisation.
- **Reproducibility artifacts:** Alignment tests and code version.

## Acceptance criteria

- [ ] Synthetic test: a bright marker at known rendered-pixel coordinates yields peak attention within 5 rendered pixels after inverse mapping.
- [ ] Attention map dimensions equal rendered_width × rendered_height (contract validation).
- [ ] On alignment failure the explanation is 'unavailable' with a reason (test).

## Verification

- `pytest tests/ml/test_gradcam_alignment.py`

## Documentation updates

- docs/model-card.md
- DESIGN.md §14 if overlay behaviour changes

## Definition of done

- UI owner verified overlay drawing with one real map.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
