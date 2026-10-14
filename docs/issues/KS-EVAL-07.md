<!-- KS-EVAL-07 | generated from docs/issues/src/05-eval.toml by scripts/backlog.py; edit the source, not this file -->
# KS-EVAL-07: Precompute cached predictions for the demo studies with full provenance

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-EVAL` |
| Workstream | evaluation |
| Recommended owner role | Evaluation with Backend reviewer |
| Status (from state.json) | blocked |

## Problem

The demo needs a fallback that works without live inference, but cached results must never look fresh.

## Expected outcome

scripts/precompute_predictions.py runs the live path once per manifest study and stores cache entries keyed by model, checkpoint, preprocessing and profile; the API serves them with source 'cached' and original computed_at.

## Dependencies

- Blocked by: `KS-API-04` — Prediction cache with provenance-preserving cached results
- Blocked by: `KS-DATA-10` — Select permitted demo studies and build the study manifest

- Blocks: `KS-DEMO-01` — Select demo cases: a correct case, an error case and a limitation

## Scope

- Use the API's live path (not a reimplementation).
- Store under the configured cache_dir.
- Verify each entry round-trips as source 'cached'.

## Explicit exclusions

- Hand-editing cache entries.

## Implementation guidance

Regenerate after any model or preprocessing version change; stale keys are cache misses by design.

## Relevant files and modules

- `scripts/precompute_predictions.py`
- `tests/api/test_cache_roundtrip.py`

## Contract impact

None (uses PredictionResponse with source 'cached').

## Acceptance criteria

- [ ] Every manifest study has a cache entry whose provenance.source is 'cached' when served and whose computed_at precedes served_at.
- [ ] Changing preprocessing version in config makes the API miss the cache (test).

## Verification

- `python scripts/precompute_predictions.py --manifest artifacts/manifest/studies.json`
- `pytest tests/api/test_cache_roundtrip.py`

## Documentation updates

- README.md 'Cached mode'
- docs/demo-script.md

## Definition of done

- Demo owner has run the cached path offline.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
