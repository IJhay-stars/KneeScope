<!-- KS-WEB-08 | generated from docs/issues/src/07-web.toml by scripts/backlog.py; edit the source, not this file -->
# KS-WEB-08: [Conditional] Client support for job-and-poll predictions

| Field | Value |
|---|---|
| Type | conditional |
| Priority | P2 |
| Epic | `KS-EPIC-WEB` |
| Workstream | frontend |
| Recommended owner role | Design/frontend |
| Status (from state.json) | conditional-pending |

> **Trigger condition:** Triggered only if KS-OPS-04 is triggered and implemented.

## Problem

If the API returns 202 with a job, the UI must poll and show progress without implying the result is live before it arrives.

## Expected outcome

Prediction client handles 202 + poll_url with backoff, shows queued/running steps, supports cancel-by-navigation, and renders the final PredictionResponse unchanged.

## Dependencies

- Blocked by: `KS-OPS-04` — [Conditional] Minimal job-and-poll inference flow

- None.

## Scope

- Polling with capped backoff.
- Timeout and error states.
- Tests with mocked 202 then 200.

## Explicit exclusions

- WebSockets/SSE.

## Implementation guidance

Keep the existing synchronous path working.

## Relevant files and modules

- `web/src/api/client.ts`
- `web/src/components/findings/`

## Contract impact

Consumes the job contract from contracts/README.md §6 (added by KS-OPS-04).

## Design references

- DESIGN.md §9.6 Run analysis

Interface work must implement the referenced DESIGN.md states exactly; if the spec must change, update DESIGN.md in the same PR.

## Acceptance criteria

- [ ] Test: 202 then 200 renders the final result with its provenance.
- [ ] Test: polling stops on unmount.
- [ ] Test: job failure shows 'Analysis failed' with code.

## Verification

- `pnpm --dir web test`

## Documentation updates

- DESIGN.md §9.6 if status text changes

## Definition of done

- Verified against the real job endpoint.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
