<!-- KS-OPS-04 | generated from docs/issues/src/08-quality.toml by scripts/backlog.py; edit the source, not this file -->
# KS-OPS-04: [Conditional] Minimal job-and-poll inference flow

| Field | Value |
|---|---|
| Type | conditional |
| Priority | P2 |
| Epic | `KS-EPIC-QUALITY` |
| Workstream | operations |
| Recommended owner role | Backend/serving |
| Status (from state.json) | conditional-pending |

> **Trigger condition:** Triggered only if KS-OPS-03 shows p95 end-to-end latency above serving.request_timeout_s on the demo hardware.

## Problem

Long synchronous requests may time out in browsers or proxies.

## Expected outcome

POST /predictions returns 202 {job_id, status, poll_url} when serving.mode='job'; GET /predictions/jobs/{job_id} returns status until the PredictionResponse is ready; implemented with an in-process worker and an in-memory/file job table, no external queue.

## Dependencies

- Blocked by: `KS-OPS-03` — Measure inference latency, peak memory and slice-serving latency

- Blocks: `KS-WEB-08` — [Conditional] Client support for job-and-poll predictions

## Scope

- Job contract added to kneescope_contracts (additive minor version).
- In-process background execution with one worker.
- Job expiry and failure states.
- Tests.

## Explicit exclusions

- Redis, Celery, external queues, multiple workers.

## Implementation guidance

Follow contracts/README.md §6 'Future job-and-poll extension'. The PredictionResponse contract does not change.

## Relevant files and modules

- `contracts/kneescope_contracts/models.py`
- `api/kneescope_api/jobs.py`
- `tests/api/test_jobs.py`
- `contracts/README.md`

## Contract impact

Adds PredictionJob model (minor version bump); consumers: web (KS-WEB-08).

## Acceptance criteria

- [ ] Test: 202 then polling returns 200 with a PredictionResponse identical in shape to the sync path.
- [ ] Test: job failure returns ApiError with INFERENCE_FAILED.
- [ ] serving.mode='sync' behaviour unchanged (existing tests pass).

## Verification

- `pytest tests/api/test_jobs.py`
- `python scripts/export_contracts.py --check`

## Documentation updates

- contracts/README.md §6
- docs/architecture.md

## Definition of done

- Web owner acknowledged the contract change.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
