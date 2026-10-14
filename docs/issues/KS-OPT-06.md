<!-- KS-OPT-06 | generated from docs/issues/src/10-optional.toml by scripts/backlog.py; edit the source, not this file -->
# KS-OPT-06: [Optional] Additional supported findings

| Field | Value |
|---|---|
| Type | optional |
| Priority | P2 |
| Epic | `KS-EPIC-MODEL` |
| Workstream | modelling |
| Recommended owner role | Modelling with Evaluation |
| Status (from state.json) | optional-blocked |

## Problem

More findings may be supportable (e.g. other RSNA labels) if labels and counts allow.

## Expected outcome

A new profile version adding findings that pass the KS-DATA-04 minimum-count rule, trained and evaluated with the same pipeline.

## Dependencies

- Blocked by: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot

- None.

## Scope

- Audit counts.
- Profile update via contract change.
- Train/evaluate.

## Explicit exclusions

- Findings without legitimate labels.

## Implementation guidance

Treat as a full repeat of MODEL-03/EVAL-03 for the new heads.

## Relevant files and modules

- `contracts/findings.json`
- `config/train.toml`

## Contract impact

findings.json profile change (contract change procedure).

## Scientific requirements

- **Dataset and label provenance:** Selected dataset.
- **Evaluation partition:** Same partitions as the baseline.
- **Applicable metrics:** Same as KS-EVAL-03.
- **What cannot be claimed:** Performance for findings below the count rule.
- **Reproducibility artifacts:** Run and snapshot for the extended model.

## Acceptance criteria

- [ ] Each added finding has audit counts meeting the rule.
- [ ] Metrics snapshot includes the new findings with counts.

## Verification

- `python scripts/export_contracts.py --check`
- `python scripts/evaluate.py ...`

## Documentation updates

- docs/decisions.md
- docs/model-card.md

## Definition of done

- Consumers acknowledged.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
