<!-- KS-DATA-03 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-03: Audit the accessible dataset(s): studies, series, planes, labels and grouping identifiers

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing |
| Status (from state.json) | blocked |

## Problem

Choosing findings and splits requires facts: how many studies have labels, per-finding positive/negative/unknown counts, which planes exist, file formats and transfer syntaxes, and whether patient or site identifiers support grouped evaluation. For RSNA only a small labelled subset exists; the remaining studies have multilingual reports only.

## Expected outcome

docs/data-audit.md §2–§6 completed for every dataset with verified access, produced by a committed script (scripts/audit_dataset.py) whose output JSON is saved under artifacts/audit/ (untracked) and summarised in the doc.

## Dependencies

- Blocked by: `KS-DATA-01` — Verify RSNA Knee data access and permitted training, hosting, demo and recording uses
- Blocked by: `KS-DATA-02` — Check alternative data sources: MRNet agreement status and organizer-provided data

- Blocks: `KS-DATA-04` — Decide the dataset and supported finding profile
- Blocks: `KS-DATA-08` — Create patient/study-grouped train, validation and test splits with leakage checks

## Scope

- Count studies, series per study, planes per study (Anatomical_Plane), slices per series, transfer syntaxes, corrupt/unreadable files.
- Per candidate finding: positive, negative, unknown/missing counts in the labelled subset.
- Whether PatientID or site can be derived for grouping; if not, state it.
- Disk size and download time for the subset to be used.

## Explicit exclusions

- No model training.
- No report text copied into the repository or issue.

## Implementation guidance

Read train.csv/train_series.csv (RSNA) with pandas or csv; open a sample of DICOMs with pydicom (+ pylibjpeg for JPEG Lossless/2000). Keep all outputs outside git (artifacts/ is ignored). Report counts only — no UIDs or report text in committed docs.

## Relevant files and modules

- `scripts/audit_dataset.py`
- `docs/data-audit.md`

## Contract impact

Provides evidence for the finding profile and preprocessing parameters; no contract change.

## Scientific requirements

- **Dataset and label provenance:** Whichever dataset(s) KS-DATA-01/02 found accessible; record version/date of download.
- **Evaluation partition:** Whole labelled pool (no splits yet).
- **Applicable metrics:** Counts and prevalence only.
- **What cannot be claimed:** Anything about model performance; that report-only studies are labelled.
- **Reproducibility artifacts:** scripts/audit_dataset.py, artifacts/audit/<dataset>.json (untracked), summary tables in docs/data-audit.md.

## Acceptance criteria

- [ ] scripts/audit_dataset.py runs on the accessible data and writes artifacts/audit/<dataset>.json.
- [ ] docs/data-audit.md has a per-finding table with positive/negative/unknown counts and the denominator (labelled studies).
- [ ] Plane availability table: count of studies with each of sagittal/coronal/axial and with none.
- [ ] Grouping section states whether patient or site identifiers exist, with the field name or 'not available'.
- [ ] Corrupt/unreadable file count and transfer-syntax breakdown are reported.

## Verification

- `python scripts/audit_dataset.py --dataset <id> --root <path> --out artifacts/audit/<id>.json`
- Second person reruns the script on the same subset and gets identical counts.

## Documentation updates

- docs/data-audit.md

## Definition of done

- Audit summary reviewed by the modelling and evaluation owners.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
