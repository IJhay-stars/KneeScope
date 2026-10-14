<!-- KS-API-02 | generated from docs/issues/src/06-api.toml by scripts/backlog.py; edit the source, not this file -->
# KS-API-02: Live inference through shared preprocessing in POST /predictions

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-API` |
| Workstream | backend |
| Recommended owner role | Backend/serving |
| Status (from state.json) | blocked |

## Problem

POST /predictions must run select_series → preprocess_study → Predictor.predict for the requested study, map outputs to the five finding states, and report provenance 'live' with measured latency — without ever reading labels.

## Expected outcome

Model-mode prediction path implemented; finding states mapped per contracts §6 (unsupported, unavailable for missing required plane, failed per finding, study-level 422 for preprocessing failures); latency measured; label isolation test extended to the API path.

## Dependencies

- Blocked by: `KS-API-01` — Dataset-backed study catalogue and slice rendering in model mode
- Blocked by: `KS-MODEL-05` — Package the checkpoint for serving with hash verification and a Predictor implementation
- Blocked by: `KS-DATA-07` — Freeze shared preprocessing v1 with visual inspection evidence

- Blocks: `KS-API-03` — Serve real explanations with alignment validation
- Blocks: `KS-API-04` — Prediction cache with provenance-preserving cached results
- Blocks: `KS-OPS-02` — Reproducible local container setup for API and web
- Blocks: `KS-OPS-03` — Measure inference latency, peak memory and slice-serving latency
- Blocks: `KS-QA-01` — End-to-end integration tests for fixture and model modes
- Blocks: `KS-DOC-01` — Reproducible README: a teammate sets up and runs inference from a clean clone
- Blocks: `KS-OPT-01` — [Optional] Upload support for user-supplied studies

## Scope

- Prediction service in api/kneescope_api/service.py for model mode.
- Predictor loaded once at startup; /healthz reports model_loaded and model_version.
- Errors mapped to ErrorCode with safe messages.
- Request timeout handling (INFERENCE_TIMEOUT, retryable).

## Explicit exclusions

- Caching (KS-API-04).
- Job-and-poll (KS-OPS-04, conditional).

## Implementation guidance

Use the tiny generated checkpoint from KS-MODEL-05 tests for CI. Do not import kneescope_ml.labels anywhere on this path.

## Relevant files and modules

- `api/kneescope_api/service.py`
- `api/kneescope_api/main.py`
- `tests/api/test_predict_live.py`
- `tests/test_label_isolation.py`

## Contract impact

None expected; PredictionResponse with source 'live'.

## Acceptance criteria

- [ ] With the tiny checkpoint, POST /predictions returns source 'live', latency_ms > 0, checkpoint_sha256 matching config, and preprocessing.version equal to config (test).
- [ ] A study missing the required plane returns all findings 'unavailable' with INPUT_INVALID (test).
- [ ] A corrupt series returns HTTP 422 PREPROCESSING_FAILED with no scores (test).
- [ ] tests/test_label_isolation.py covers the model-mode prediction path and passes.
- [ ] /healthz reports model_loaded true and the model_version.

## Verification

- `pytest tests/api tests/test_label_isolation.py`

## Documentation updates

- docs/architecture.md (request flow)
- contracts/README.md §6 if clarified

## Definition of done

- Frontend shows a live result with the LIVE badge against this endpoint.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
