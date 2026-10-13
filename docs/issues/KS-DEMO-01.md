<!-- KS-DEMO-01 | generated from docs/issues/src/09-delivery.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DEMO-01: Select demo cases: a correct case, an error case and a limitation

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-DELIVERY` |
| Workstream | delivery |
| Recommended owner role | Design/frontend (demo owner) with Evaluation |
| Status (from state.json) | blocked |

## Problem

The plan requires the demo to show a correct case, an error case and a limitation, using permitted studies from the evaluation partition.

## Expected outcome

docs/demo-script.md lists the chosen study IDs (manifest IDs only), why each was chosen, the expected screen at each step, and the evidence that the 'correct' case is correct per its dataset label.

## Dependencies

- Blocked by: `KS-EVAL-04` — Error analysis: false positives, false negatives and failure cases
- Blocked by: `KS-EVAL-07` — Precompute cached predictions for the demo studies with full provenance
- Blocked by: `KS-DATA-10` — Select permitted demo studies and build the study manifest

- Blocks: `KS-DEMO-02` — Demo script and rehearsal

## Scope

- Pick from the manifest and error analysis.
- Include a missing-series or failure state.
- Include a limitation (e.g. weak finding, undefined AUC, explanation caveat).

## Explicit exclusions

- Cherry-picking presented as typical performance.

## Implementation guidance

State on screen or in narration that cases were selected for illustration.

## Relevant files and modules

- `docs/demo-script.md`

## Contract impact

None.

## Acceptance criteria

- [ ] Three cases listed with roles (correct, error, limitation) and their partition.
- [ ] Each case runs in cached mode offline (checked).

## Verification

- Manual run-through in cached mode recorded in the PR.

## Documentation updates

- docs/demo-script.md

## Definition of done

- Evaluation owner agrees cases are fairly described.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
