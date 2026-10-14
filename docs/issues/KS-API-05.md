<!-- KS-API-05 | generated from docs/issues/src/06-api.toml by scripts/backlog.py; edit the source, not this file -->
# KS-API-05: Serve real labels, metrics snapshot and model card

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-API` |
| Workstream | backend |
| Recommended owner role | Backend/serving |
| Status (from state.json) | blocked |

## Problem

In model mode /studies/{id}/labels, /metrics and /model-card must serve the real artifacts, keeping labels out of the prediction path.

## Expected outcome

Label store reads the KS-LABEL-01 file; /metrics serves the KS-EVAL-03 snapshot for the loaded model_version (or 'unavailable' if missing); /model-card serves the published card.

## Dependencies

- Blocked by: `KS-API-01` — Dataset-backed study catalogue and slice rendering in model mode
- Blocked by: `KS-LABEL-01` — Build the labels file with provenance and explicit unknown handling
- Blocked by: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot
- Blocked by: `KS-EVAL-06` — Complete the model card from evaluated evidence

- Blocks: `KS-QA-02` — Independent completion review against the evidence-based definition of done

## Scope

- Artifact paths via settings.
- Version match: metrics/model card must match the loaded model_version, otherwise 'unavailable' with reason.
- Tests with generated artifacts.

## Explicit exclusions

- Editing metrics in the API.

## Implementation guidance

A snapshot for a different model_version is never served as current.

## Relevant files and modules

- `api/kneescope_api/store.py`
- `api/kneescope_api/main.py`
- `tests/api/test_artifacts.py`

## Contract impact

None.

## Acceptance criteria

- [ ] Metrics snapshot whose model_version differs from the loaded model returns status 'unavailable' with a reason (test).
- [ ] Labels endpoint returns provenance per label (test).
- [ ] tests/test_label_isolation.py passes.

## Verification

- `pytest tests/api/test_artifacts.py tests/test_label_isolation.py`

## Documentation updates

- README.md

## Definition of done

- Evaluation page renders the real snapshot.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
