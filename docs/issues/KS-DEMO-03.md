<!-- KS-DEMO-03 | generated from docs/issues/src/09-delivery.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DEMO-03: Recorded fallback demonstration within data-use terms

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-DELIVERY` |
| Workstream | delivery |
| Recommended owner role | Design/frontend (demo owner) |
| Status (from state.json) | blocked |

## Problem

A recording protects against live failure, but recordings of restricted images may count as making data available.

## Expected outcome

A recording of the scripted demo, stored where the permitted-use table allows (local only if unclear), with a note of the permission basis; if recording images is not permitted, a recording in fixture mode plus narrated results.

## Dependencies

- Blocked by: `KS-DEMO-02` — Demo script and rehearsal
- Blocked by: `KS-DATA-01` — Verify RSNA Knee data access and permitted training, hosting, demo and recording uses

- Blocks: `KS-DEL-01` — Assemble and submit the final delivery package

## Scope

- Record per script.
- Store per permission.
- Note permission basis.

## Explicit exclusions

- Uploading to public platforms without permission and coordinator approval.

## Implementation guidance

Check KS-DATA-01 'recording' row before recording real slices.

## Relevant files and modules

- `docs/demo-script.md`

## Contract impact

None.

## Acceptance criteria

- [ ] docs/demo-script.md 'Recording' section states file location, mode (dataset or fixture), permission basis, and who approved sharing.
- [ ] Recording plays end to end (checked by a second person).

## Verification

- Second person playback check noted in the issue.

## Documentation updates

- docs/demo-script.md

## Definition of done

- Stored according to permission.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
