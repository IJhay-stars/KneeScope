<!-- KS-SCOPE-03 | generated from docs/issues/src/01-scope.toml by scripts/backlog.py; edit the source, not this file -->
# KS-SCOPE-03: [Conditional] Deliver as an interaction prototype if no usable training data exists

| Field | Value |
|---|---|
| Type | conditional |
| Priority | P0 |
| Epic | `KS-EPIC-SCOPE` |
| Workstream | coordination |
| Recommended owner role | Coordinator/integrator |
| Status (from state.json) | conditional-pending |

> **Trigger condition:** Triggered only if KS-DATA-04 records that no dataset with verified access and usable labels is available in time.

## Problem

Without permitted training data there can be no real model. The product must then be presented honestly as an interaction prototype, with no detection claims and no numbers that look like results.

## Expected outcome

The app, README, model card and demo state that KneeScope is an interaction prototype; model, evaluation and cached-prediction issues are closed as 'not applicable' with a link to the decision; fixture mode is the documented run mode.

## Dependencies

- Blocked by: `KS-DATA-04` — Decide the dataset and supported finding profile

- None.

## Scope

- Set findings profile 'interaction_prototype' as the documented mode.
- Update README, model card draft and demo script wording.
- Close or relabel MODEL, EVAL-02..07, API-02..04 issues as not applicable with links.

## Explicit exclusions

- No placeholder scores presented as results.
- No metrics page numbers.

## Implementation guidance

The fixture banner, hatch pattern and 'FIXTURE — not a model output' text already exist; verify they appear on every result surface. The demo then shows the workflow, the states, and the limitations.

## Relevant files and modules

- `README.md`
- `docs/model-card.md`
- `docs/demo-script.md`
- `contracts/findings.json`

## Contract impact

None (uses existing interaction_prototype profile).

## Acceptance criteria

- [ ] README first paragraph states 'interaction prototype' and 'no model'.
- [ ] Every prediction shown in the UI carries the FIXTURE badge (checked on all four fixture studies).
- [ ] GET /metrics returns status 'unavailable'.
- [ ] Each not-applicable issue links to the KS-DATA-04 decision.

## Verification

- `curl -s localhost:8000/metrics | grep '"unavailable"'`
- `pnpm --dir web test`

## Documentation updates

- README.md
- docs/model-card.md
- docs/demo-script.md
- docs/issue-index.md

## Definition of done

- Decision link present on every closed-as-not-applicable issue.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
