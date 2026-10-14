<!-- KS-QA-02 | generated from docs/issues/src/09-delivery.toml by scripts/backlog.py; edit the source, not this file -->
# KS-QA-02: Independent completion review against the evidence-based definition of done

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DELIVERY` |
| Workstream | qa |
| Recommended owner role | Independent reviewer/QA |
| Status (from state.json) | blocked |

## Problem

Issues get closed because code exists. The plan defines completion through evidence (plan §10).

## Expected outcome

docs/completion-review.md checks each plan §10 criterion with a link to evidence, and lists any gap as an open issue; the review is done by someone who did not implement the checked item.

## Dependencies

- Blocked by: `KS-QA-01` — End-to-end integration tests for fixture and model modes
- Blocked by: `KS-EVAL-06` — Complete the model card from evaluated evidence
- Blocked by: `KS-API-05` — Serve real labels, metrics snapshot and model card
- Blocked by: `KS-API-03` — Serve real explanations with alignment validation
- Blocked by: `KS-WEB-07` — Accessibility and responsive verification across all pages
- Blocked by: `KS-OPS-01` — Restricted-asset protection: data, checkpoints, logs and repository guards
- Blocked by: `KS-DEMO-02` — Demo script and rehearsal

- Blocks: `KS-DEL-01` — Assemble and submit the final delivery package

## Scope

- Plan §10 checklist: reproducible README; same preprocessing for selected studies; real checkpoint outputs displayed; cached outputs identify source and checkpoint; clear errors for missing/malformed inputs; held-out evaluation with counts and split method; legitimate label source per finding; explanations aligned or omitted; data and model assets used within permissions; demo shows correct case, error case and limitation.
- Contract agreement: export --check, web gen:api:check.
- Scientific guardrails review (AGENTS.md).

## Explicit exclusions

- Fixing issues found (file them).

## Implementation guidance

Mark each item pass/fail with evidence link; 'fail' blocks KS-DEL-01.

## Relevant files and modules

- `docs/completion-review.md`

## Contract impact

None.

## Acceptance criteria

- [ ] Every plan §10 criterion has pass/fail and an evidence link.
- [ ] All guardrails in AGENTS.md 'Scientific and product guardrails' reviewed with pass/fail.
- [ ] Failures are linked to open issues.

## Verification

- `python scripts/backlog.py check`
- `python scripts/export_contracts.py --check`
- `pnpm --dir web gen:api:check`

## Documentation updates

- docs/completion-review.md

## Definition of done

- No 'fail' remains unaddressed before KS-DEL-01.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
