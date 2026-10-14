<!-- KS-SCOPE-01 | generated from docs/issues/src/01-scope.toml by scripts/backlog.py; edit the source, not this file -->
# KS-SCOPE-01: Confirm organizer submission requirements, judging criteria and deadline

| Field | Value |
|---|---|
| Type | decision |
| Priority | P0 |
| Epic | `KS-EPIC-SCOPE` |
| Workstream | coordination |
| Recommended owner role | Coordinator/integrator (human decision) |
| Status (from state.json) | ready |

## Problem

The PRD (§17.8) leaves open what must be submitted (repository, live link, video, slides), by what hour, and how the hackathon is judged. Delivery, deployment and demo issues cannot define 'done' without this.

## Expected outcome

docs/decisions.md contains a decision entry quoting the organizer's actual requirements (source, date, who confirmed), and docs/issue-index.md marks which conditional delivery issues (KS-OPS-05 deployment, KS-DEMO-03 recording) are triggered.

## Dependencies

- None — can start now.

- Blocks: `KS-OPS-05` — [Conditional] Permitted deployment of a hosted demo
- Blocks: `KS-DEL-01` — Assemble and submit the final delivery package

## Scope

- Ask the organizers (or read their published brief) for required deliverables, format, deadline with timezone, and judging criteria.
- Record whether a public live link is required or only a repository/demo.
- Record any rules about data, recordings or third-party datasets.

## Explicit exclusions

- Do not accept terms, register the team, or submit anything on anyone's behalf as part of this issue.
- Do not create a slide deck (separate task outside this backlog).

## Implementation guidance

Quote the organizer source verbatim in the decision entry (link or message reference, no personal contact details). If requirements are unknown, record 'unknown' explicitly and list the follow-up owner; do not assume a live deployment is required.

## Relevant files and modules

- `docs/decisions.md`
- `docs/issue-index.md`

## Contract impact

None.

## Acceptance criteria

- [ ] docs/decisions.md has an entry 'Organizer requirements' listing each required deliverable, the deadline with timezone, and judging criteria, each with a source reference or the word 'unknown'.
- [ ] KS-OPS-05 and KS-DEMO-03 are marked 'triggered' or 'not triggered' in docs/issue-index.md with a link to the decision entry.
- [ ] KS-DEL-01 body is updated with the concrete deliverable checklist.

## Verification

- Reviewer reads the decision entry and confirms each item has a source or 'unknown'.
- `python scripts/backlog.py check`

## Documentation updates

- docs/decisions.md
- docs/issue-index.md

## Definition of done

- Decision recorded and linked from KS-DEL-01.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
