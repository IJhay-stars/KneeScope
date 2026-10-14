<!-- KS-OPT-03 | generated from docs/issues/src/10-optional.toml by scripts/backlog.py; edit the source, not this file -->
# KS-OPT-03: [Optional] Exploratory threshold slider per finding

| Field | Value |
|---|---|
| Type | optional |
| Priority | P2 |
| Epic | `KS-EPIC-WEB` |
| Workstream | frontend |
| Recommended owner role | Design/frontend with Evaluation reviewer |
| Status (from state.json) | optional-blocked |

## Problem

PRD lists a threshold slider as 'should ship'. It helps show trade-offs but can suggest that any threshold is validated.

## Expected outcome

On the evaluation page only, a slider per finding showing sensitivity/specificity at the chosen threshold from precomputed validation operating points, with the validated threshold marked.

## Dependencies

- Blocked by: `KS-EVAL-02` — Select per-finding operating thresholds on the validation partition
- Blocked by: `KS-WEB-06` — Evaluation and model-card ledger view

- None.

## Scope

- Operating points exported by evaluation.
- Slider on evaluation page.
- Label 'exploratory'.

## Explicit exclusions

- Changing thresholds used by predictions in the review view.

## Implementation guidance

Operating points come from validation only.

## Relevant files and modules

- `web/src/components/ledger/ThresholdExplorer.tsx`
- `ml/kneescope_ml/evaluation.py`

## Contract impact

Adds optional operating_points to FindingMetrics (minor version).

## Design references

- DESIGN.md §9.11

Interface work must implement the referenced DESIGN.md states exactly; if the spec must change, update DESIGN.md in the same PR.

## Acceptance criteria

- [ ] Slider values match exported operating points (test).
- [ ] Review-view predictions unaffected (test).

## Verification

- `pnpm --dir web test`
- `pytest tests/ml/test_evaluation.py`

## Documentation updates

- DESIGN.md §9.11
- contracts/README.md §9

## Definition of done

- Evaluation owner reviewed wording.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
