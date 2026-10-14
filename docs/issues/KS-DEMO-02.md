<!-- KS-DEMO-02 | generated from docs/issues/src/09-delivery.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DEMO-02: Demo script and rehearsal

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-DELIVERY` |
| Workstream | delivery |
| Recommended owner role | Design/frontend (demo owner) |
| Status (from state.json) | blocked |

## Problem

The presentation narrative (plan p.8, PRD §17.6) must run in about three minutes: inspect a study, run inference, review a finding, reveal its label, show evaluation, explain a failure, name limits.

## Expected outcome

docs/demo-script.md with timed steps, spoken claims checked against the model card, fallback switch points (live → cached → recording), and at least one full timed rehearsal noted.

## Dependencies

- Blocked by: `KS-DEMO-01` — Select demo cases: a correct case, an error case and a limitation
- Blocked by: `KS-WEB-07` — Accessibility and responsive verification across all pages
- Blocked by: `KS-API-04` — Prediction cache with provenance-preserving cached results
- Blocked by: `KS-WEB-06` — Evaluation and model-card ledger view

- Blocks: `KS-DEMO-03` — Recorded fallback demonstration within data-use terms
- Blocks: `KS-QA-02` — Independent completion review against the evidence-based definition of done

## Scope

- Write the script.
- Rehearse live and in cached mode.
- Check every spoken claim against artifacts.

## Explicit exclusions

- Slide deck (separate task).

## Implementation guidance

Banned phrasing: 'detects tears', 'accuracy' for AUC, 'probability' for uncalibrated scores, 'shows where the tear is'.

## Relevant files and modules

- `docs/demo-script.md`

## Contract impact

None.

## Acceptance criteria

- [ ] Script steps each list the screen, the action, and the claim with its source artifact.
- [ ] Rehearsal log with duration ≤ the organizer's limit (or 3 minutes if unknown).
- [ ] Fallback triggers defined (e.g. live call > 10 s → switch to cached).

## Verification

- Rehearsal recorded in the PR (time and issues found).

## Documentation updates

- docs/demo-script.md

## Definition of done

- QA role reviewed claims.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
