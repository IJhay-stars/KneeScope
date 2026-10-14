<!-- KS-DOC-01 | generated from docs/issues/src/09-delivery.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DOC-01: Reproducible README: a teammate sets up and runs inference from a clean clone

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DELIVERY` |
| Workstream | delivery |
| Recommended owner role | Coordinator/integrator with a teammate as tester |
| Status (from state.json) | blocked |

## Problem

The plan's first completion criterion: a teammate can reproduce setup and inference from the README.

## Expected outcome

README covers prerequisites, fixture mode, data placement (without redistributing data), checkpoint placement and hash check, model mode, cached mode, tests, and troubleshooting; a teammate who did not write it follows it on a clean machine and records the result.

## Dependencies

- Blocked by: `KS-API-02` — Live inference through shared preprocessing in POST /predictions
- Blocked by: `KS-MODEL-05` — Package the checkpoint for serving with hash verification and a Predictor implementation
- Blocked by: `KS-OPS-02` — Reproducible local container setup for API and web

- Blocks: `KS-DEL-01` — Assemble and submit the final delivery package

## Scope

- Update README sections.
- Clean-clone test by someone else; capture commands and timings.
- Fix every gap found.

## Explicit exclusions

- Instructions that require private credentials in files.

## Implementation guidance

Commands must be copy-pasteable. Data download steps point to the official source and require each person to accept terms themselves.

## Relevant files and modules

- `README.md`
- `docs/reproducibility.md`

## Contract impact

None.

## Acceptance criteria

- [ ] docs/reproducibility.md contains a dated log from a teammate (not the author) showing fixture mode and model mode working from a clean clone, with commands run.
- [ ] scripts/check_docs.py passes (no broken local links, no placeholders).

## Verification

- `python scripts/check_docs.py`

## Documentation updates

- README.md
- docs/reproducibility.md

## Definition of done

- Tester's name and date recorded.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
