<!-- KS-API-03 | generated from docs/issues/src/06-api.toml by scripts/backlog.py; edit the source, not this file -->
# KS-API-03: Serve real explanations with alignment validation

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-API` |
| Workstream | backend |
| Recommended owner role | Backend/serving with Labels reviewer |
| Status (from state.json) | blocked |

## Problem

GET /studies/{id}/explanations/{finding} must return explanations produced for the same prediction and checkpoint, or 'unavailable' — never a stale or mismatched overlay.

## Expected outcome

Explanations computed with (or stored alongside) the prediction, keyed by prediction_id; the endpoint validates study, finding, prediction_id and model_version and returns 'unavailable' with a reason on any mismatch.

## Dependencies

- Blocked by: `KS-API-02` — Live inference through shared preprocessing in POST /predictions
- Blocked by: `KS-LABEL-03` — Influential-slice explanations aligned to series slice coordinates

- Blocks: `KS-QA-02` — Independent completion review against the evidence-based definition of done

## Scope

- Store explanation outputs per prediction_id (in-memory or alongside cache).
- Validation of identifiers and rendered size.
- Tests for mismatch paths.

## Explicit exclusions

- Generating overlays client-side.

## Implementation guidance

An unknown prediction_id returns status 'unavailable' (reason EXPLANATION_UNAVAILABLE), not a 500.

## Relevant files and modules

- `api/kneescope_api/service.py`
- `tests/api/test_explanations.py`

## Contract impact

None (Explanation).

## Acceptance criteria

- [ ] Explanation for a live prediction validates and its slice indices are within the series range (test).
- [ ] Mismatched prediction_id returns status 'unavailable' with reason (test).
- [ ] explanation_available in FindingResult is true only when an explanation exists (test).

## Verification

- `pytest tests/api/test_explanations.py`

## Documentation updates

- contracts/README.md §7 if clarified

## Definition of done

- UI influential-slice jump verified against it.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
