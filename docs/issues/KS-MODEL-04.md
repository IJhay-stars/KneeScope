<!-- KS-MODEL-04 | generated from docs/issues/src/04-model.toml by scripts/backlog.py; edit the source, not this file -->
# KS-MODEL-04: [Conditional] One improvement round (fine-tuning or adjacent-slice input)

| Field | Value |
|---|---|
| Type | conditional |
| Priority | P2 |
| Epic | `KS-EPIC-MODEL` |
| Workstream | modelling |
| Recommended owner role | Modelling |
| Status (from state.json) | conditional-pending |

> **Trigger condition:** Triggered only if KS-EVAL-03 shows the baseline is clearly above the comparator on validation and compute remains for at least one full additional run.

## Problem

Fine-tuning the encoder or adjacent-slice stacks may help, but each extra run costs compute and invites validation overfitting.

## Expected outcome

At most one pre-declared improvement experiment, selected on validation, with the same reporting as the baseline; the served checkpoint changes only if the improvement is recorded and the test partition remains untouched until final evaluation.

## Dependencies

- Blocked by: `KS-MODEL-03` — Train the baseline model on the selected dataset
- Blocked by: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot

- None.

## Scope

- Declare the single change before running.
- Same splits, same metrics.

## Explicit exclusions

- Ensembles, TTA, hyperparameter sweeps.

## Implementation guidance

If the improvement is within noise, keep the baseline. Record both in docs/experiments.md.

## Relevant files and modules

- `config/train.toml`
- `docs/experiments.md`

## Contract impact

May change model_version; cached predictions must be regenerated.

## Scientific requirements

- **Dataset and label provenance:** Same as KS-MODEL-03.
- **Evaluation partition:** Validation for selection.
- **Applicable metrics:** Per-finding ROC AUC with counts.
- **What cannot be claimed:** That a validation difference generalises.
- **Reproducibility artifacts:** Second run directory and comparison.

## Acceptance criteria

- [ ] Pre-declared hypothesis committed before the run (docs/experiments.md entry timestamped).
- [ ] Validation comparison table baseline vs improved with counts.
- [ ] Decision entry on which checkpoint is served.

## Verification

- `python scripts/train.py --config config/train-improve.toml`

## Documentation updates

- docs/experiments.md
- docs/decisions.md

## Definition of done

- Served checkpoint decision recorded.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
