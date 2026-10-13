<!-- KS-LABEL-02 | generated from docs/issues/src/03-labels.toml by scripts/backlog.py; edit the source, not this file -->
# KS-LABEL-02: [Conditional] Extract labels from radiology reports with negation, uncertainty and provenance

| Field | Value |
|---|---|
| Type | conditional |
| Priority | P1 |
| Epic | `KS-EPIC-LABELS` |
| Workstream | labels |
| Recommended owner role | Labels/explainability |
| Status (from state.json) | conditional-pending |

> **Trigger condition:** Triggered only if KS-DATA-04 records that the provided labelled subset is too small for the selected findings and that report extraction is permitted and worth the effort.

## Problem

RSNA provides multilingual free-text reports for studies without labels. Extracted labels could enlarge training data but introduce noise; negation, uncertainty and language must be handled, and reports must never become an inference input.

## Expected outcome

A versioned, rule-based (or documented model-based) extractor producing report_extracted labels with rule version in source_ref, a manual spot-check sample with agreement figures against the provided labels, and a decision on whether extracted labels are used for training only (never for evaluation).

## Dependencies

- Blocked by: `KS-DATA-04` — Decide the dataset and supported finding profile
- Blocked by: `KS-LABEL-01` — Build the labels file with provenance and explicit unknown handling

- None.

## Scope

- Extractor with per-language patterns or a permitted translation step run locally.
- Negation and uncertainty → negative/unknown rules.
- Spot check ≥50 reports per language group present, plus agreement vs provided labels on the overlapping subset.
- Training-only use flag.

## Explicit exclusions

- Evaluation partitions use provided expert/dataset labels only.
- No report text in the repository, logs or issues.
- No upload of reports to external APIs without verified permission.

## Implementation guidance

The original report must not be available at inference. Store extracted labels with provenance report_extracted and source_ref 'rules vX.Y'.

## Relevant files and modules

- `ml/kneescope_ml/report_labels.py`
- `scripts/extract_report_labels.py`
- `tests/ml/test_report_labels.py`
- `docs/data-audit.md`

## Contract impact

Uses LabelProvenance.report_extracted (already in contract).

## Scientific requirements

- **Dataset and label provenance:** RSNA reports for unlabelled training studies.
- **Evaluation partition:** Training only.
- **Applicable metrics:** Agreement (per-class) against provided labels on overlap; spot-check error rate.
- **What cannot be claimed:** That extracted labels equal expert labels; any evaluation result computed on extracted labels.
- **Reproducibility artifacts:** Extractor version, spot-check sheet (local), agreement table.

## Acceptance criteria

- [ ] Unit tests cover negation ('no ACL tear'), uncertainty ('possible tear'), and at least two languages present in the data.
- [ ] Agreement table (per finding, per language group) vs provided labels committed to docs/data-audit.md with sample sizes.
- [ ] A test fails if any evaluation partition label has provenance report_extracted.
- [ ] Extractor version recorded in every extracted label's source_ref.

## Verification

- `pytest tests/ml/test_report_labels.py`
- `python scripts/extract_report_labels.py --sample 50 --spot-check`

## Documentation updates

- docs/data-audit.md §3
- docs/model-card.md
- docs/decisions.md

## Definition of done

- Decision entry states whether extracted labels are used and why.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
