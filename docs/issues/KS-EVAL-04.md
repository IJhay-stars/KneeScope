<!-- KS-EVAL-04 | generated from docs/issues/src/05-eval.toml by scripts/backlog.py; edit the source, not this file -->
# KS-EVAL-04: Error analysis: false positives, false negatives and failure cases

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-EVAL` |
| Workstream | evaluation |
| Recommended owner role | Evaluation with Labels reviewer |
| Status (from state.json) | blocked |

## Problem

Numbers alone do not show how the model fails. The demo must include an honest failure case, and the model card must list known failure modes.

## Expected outcome

docs/error-analysis.md with categorised FP/FN examples (by study ID only, no patient data), patterns observed (e.g. missing planes, protocol differences), and subgroup results only where metadata and counts support them.

## Dependencies

- Blocked by: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot

- Blocks: `KS-EVAL-06` — Complete the model card from evaluated evidence
- Blocks: `KS-DEMO-01` — Select demo cases: a correct case, an error case and a limitation

## Scope

- Review top-scoring negatives and lowest-scoring positives per finding.
- Categorise causes; note label quality issues.
- Pick candidate failure cases for the demo.
- Subgroups only with stated minimum counts.

## Explicit exclusions

- Clinical interpretation of images beyond what labels state.

## Implementation guidance

Screenshots of restricted data stay local unless the permitted-use table allows sharing.

## Relevant files and modules

- `docs/error-analysis.md`
- `scripts/error_analysis.py`

## Contract impact

None.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset.
- **Evaluation partition:** Same partition as KS-EVAL-03.
- **Applicable metrics:** Counts per error category.
- **What cannot be claimed:** Causal explanations for model errors.
- **Reproducibility artifacts:** Case list (IDs only), categories, script.

## Acceptance criteria

- [ ] At least 5 FP and 5 FN (or all, if fewer) reviewed per retained finding with a category each.
- [ ] Failure modes summarised in the model card limitations.
- [ ] Subgroup table either present with counts ≥ the stated minimum or explicitly omitted with reason.

## Verification

- `python scripts/error_analysis.py --run <run_id> --split <partition>`

## Documentation updates

- docs/error-analysis.md
- docs/model-card.md

## Definition of done

- Demo owner has the candidate failure cases.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
