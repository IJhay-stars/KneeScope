<!-- KS-SCOPE-02 | generated from docs/issues/src/01-scope.toml by scripts/backlog.py; edit the source, not this file -->
# KS-SCOPE-02: Agree named owners per workstream and record collaboration boundaries

| Field | Value |
|---|---|
| Type | decision |
| Priority | P0 |
| Epic | `KS-EPIC-SCOPE` |
| Workstream | coordination |
| Recommended owner role | Coordinator/integrator (human decision) |
| Status (from state.json) | ready |

## Problem

The project plan proposes ownership by deliverable but notes it is a recommendation, not an accepted assignment. Integration ownership must not silently become responsibility for data, training, backend and everyone's unfinished work.

## Expected outcome

The ownership table in AGENTS.md ('Workstreams and ownership') names an accountable person (or 'unassigned') per workstream, with merged roles stated for a team smaller than six, and each person has confirmed their row.

## Dependencies

- None — can start now.

- None.

## Scope

- Fill the owner column of the AGENTS.md workstream table.
- Record merged roles if the team is smaller than six (PRD §17.4 merge pattern or an agreed alternative).
- Name a reviewer from a different workstream for each workstream.

## Explicit exclusions

- Do not assign issues to people who have not agreed to them.

## Implementation guidance

Use the role names already in AGENTS.md. Record agreement as a short decision entry with date. Unassigned workstreams stay visibly unassigned; the coordinator does not inherit them by default.

## Relevant files and modules

- `AGENTS.md`
- `docs/decisions.md`

## Contract impact

None.

## Acceptance criteria

- [ ] Every row of the AGENTS.md ownership table has a named owner or the literal text 'unassigned'.
- [ ] Each named owner has confirmed (decision entry lists confirmations with date).
- [ ] Each workstream has a named cross-workstream reviewer or 'unassigned'.

## Verification

- Reviewer checks the table against the decision entry.

## Documentation updates

- AGENTS.md
- docs/decisions.md

## Definition of done

- Ownership table merged to main.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
