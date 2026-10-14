<!-- KS-QA-01 | generated from docs/issues/src/08-quality.toml by scripts/backlog.py; edit the source, not this file -->
# KS-QA-01: End-to-end integration tests for fixture and model modes

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-QUALITY` |
| Workstream | qa |
| Recommended owner role | Independent reviewer/QA |
| Status (from state.json) | blocked |

## Problem

Unit tests on each side do not prove the workflow works together: select a study, view slices, run analysis, see provenance, reveal a label, open evaluation.

## Expected outcome

An automated end-to-end check (Playwright or a scripted HTTP + DOM test) running the full workflow against fixture mode in CI and against model mode with the tiny test checkpoint, plus contract agreement checks between API responses and web types.

## Dependencies

- Blocked by: `KS-API-02` — Live inference through shared preprocessing in POST /predictions
- Blocked by: `KS-WEB-03` — Findings panel: run analysis, five finding states and result provenance

- Blocks: `KS-QA-02` — Independent completion review against the evidence-based definition of done

## Scope

- E2E workflow test.
- Model-mode run in CI with generated synthetic DICOM and tiny checkpoint.
- Assert provenance badges match API source.

## Explicit exclusions

- Visual regression tooling.

## Implementation guidance

Playwright is acceptable if its browser download works in CI; otherwise use the API + Vitest DOM test approach and record why.

## Relevant files and modules

- `tests/e2e/`
- `.github/workflows/ci.yml`

## Contract impact

None.

## Acceptance criteria

- [ ] CI job runs the workflow in fixture mode and asserts the FIXTURE badge and five-state rendering.
- [ ] CI job runs model mode with the tiny checkpoint and asserts the LIVE badge and latency.
- [ ] Failure of any step fails CI.

## Verification

- `pnpm --dir tests/e2e test (or documented command)`
- GitHub Actions run link

## Documentation updates

- README.md 'Testing'
- AGENTS.md verification table if commands change

## Definition of done

- Green CI run linked.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
