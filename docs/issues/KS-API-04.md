<!-- KS-API-04 | generated from docs/issues/src/06-api.toml by scripts/backlog.py; edit the source, not this file -->
# KS-API-04: Prediction cache with provenance-preserving cached results

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-API` |
| Workstream | backend |
| Recommended owner role | Backend/serving |
| Status (from state.json) | blocked |

## Problem

A cached mode is the operational fallback for the demo, but cached outputs must never masquerade as live inference, and stale entries (different model or preprocessing) must never be served.

## Expected outcome

File-based cache under serving.cache_dir keyed by study_id, model_version, checkpoint_sha256, preprocessing version and profile; served with source 'cached', original computed_at, cache_key, no latency; allow_cached=false forces live.

## Dependencies

- Blocked by: `KS-API-02` — Live inference through shared preprocessing in POST /predictions

- Blocks: `KS-EVAL-07` — Precompute cached predictions for the demo studies with full provenance
- Blocks: `KS-DEMO-02` — Demo script and rehearsal

## Scope

- Cache write after live runs (opt-in flag) and read on request.
- Key mismatch = miss.
- Study list analysis_status 'cached' when an entry exists.
- Tests.

## Explicit exclusions

- Redis or any external store.

## Implementation guidance

Cache files may contain study IDs; keep cache_dir untracked and out of public hosting unless permitted.

## Relevant files and modules

- `api/kneescope_api/cache.py`
- `api/kneescope_api/service.py`
- `tests/api/test_cache.py`

## Contract impact

None (ResultProvenance cached rules already enforced).

## Acceptance criteria

- [ ] Served cached result has source 'cached', computed_at from the original run, cache_key set, latency_ms null (test).
- [ ] Changing model_version or preprocessing version yields a miss and a live run (test).
- [ ] allow_cached=false always returns 'live' (test).
- [ ] A tampered cache entry that fails contract validation is ignored and logged without content (test).

## Verification

- `pytest tests/api/test_cache.py`

## Documentation updates

- README.md 'Cached mode'
- docs/architecture.md

## Definition of done

- Frontend shows CACHED badge with timestamp for a cached result.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
