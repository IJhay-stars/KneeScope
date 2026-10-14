<!-- KS-OPS-05 | generated from docs/issues/src/08-quality.toml by scripts/backlog.py; edit the source, not this file -->
# KS-OPS-05: [Conditional] Permitted deployment of a hosted demo

| Field | Value |
|---|---|
| Type | conditional |
| Priority | P2 |
| Epic | `KS-EPIC-QUALITY` |
| Workstream | operations |
| Recommended owner role | Backend/serving with Coordinator approval |
| Status (from state.json) | conditional-pending |

> **Trigger condition:** Triggered only if KS-SCOPE-01 shows the organizers require a live link AND the KS-DATA-01/02 permitted-use table allows public hosting of the images to be shown (otherwise fixture-mode-only hosting, or no hosting).

## Problem

A public link may be required, but competition data may not be made available to non-participants.

## Expected outcome

A hosted deployment on a free or already-approved platform, serving only content the terms allow (possibly fixture mode only), with access restrictions if required; approved by the coordinator before going public.

## Dependencies

- Blocked by: `KS-SCOPE-01` — Confirm organizer submission requirements, judging criteria and deadline
- Blocked by: `KS-DATA-04` — Decide the dataset and supported finding profile
- Blocked by: `KS-OPS-01` — Restricted-asset protection: data, checkpoints, logs and repository guards
- Blocked by: `KS-OPS-02` — Reproducible local container setup for API and web

- None.

## Scope

- Choose platform without new paid subscriptions unless approved.
- Deploy the container from KS-OPS-02.
- Verify what is publicly reachable.

## Explicit exclusions

- Publishing restricted data.
- Spending money or accepting platform terms without human approval.

## Implementation guidance

An agent prepares the deployment but a human approves and performs the publish step.

## Relevant files and modules

- `docs/deployment.md`

## Contract impact

None.

## Acceptance criteria

- [ ] docs/deployment.md lists exactly what is hosted, the permission basis, and who approved.
- [ ] From an unauthenticated browser, only permitted content is reachable (checked list of URLs).
- [ ] /healthz reports the expected mode.

## Verification

- `curl -fs https://<host>/healthz`

## Documentation updates

- docs/deployment.md
- README.md

## Definition of done

- Coordinator approval recorded.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
