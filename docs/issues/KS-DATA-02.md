<!-- KS-DATA-02 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-02: Check alternative data sources: MRNet agreement status and organizer-provided data

| Field | Value |
|---|---|
| Type | decision |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing (human decision) |
| Status (from state.json) | ready |

## Problem

If RSNA access, labels or terms are unsuitable, the fallback options are MRNet (requires an approved data-use agreement; supports overall abnormality, ACL tear and meniscal tear only) or data supplied by the hackathon organizers (supports only its documented labels).

## Expected outcome

docs/data-audit.md §1 has equivalent permitted-use rows for MRNet and for organizer data (or 'not offered'), with agreement status and turnaround.

## Dependencies

- None — can start now.

- Blocks: `KS-DATA-03` — Audit the accessible dataset(s): studies, series, planes, labels and grouping identifiers

## Scope

- Record MRNet registration/agreement status and terms on training, hosting, demo and recording.
- Ask organizers whether they provide data and under what terms.
- Record label lists each source actually provides.

## Explicit exclusions

- Do not submit agreements or register accounts on anyone's behalf.
- Do not invent MCL or medial/lateral meniscus labels for MRNet.

## Implementation guidance

MRNet tasks map to finding IDs abnormal, acl_tear, meniscal_tear in contracts/findings.json. Organizer data needs its own profile only after KS-DATA-03 audits it.

## Relevant files and modules

- `docs/data-audit.md`

## Contract impact

May later add an organizer profile to contracts/findings.json (via KS-DATA-04).

## Scientific requirements

- **Dataset and label provenance:** MRNet (Stanford ML Group) under its research use agreement; organizer data under its stated terms.
- **Evaluation partition:** Not applicable.
- **Applicable metrics:** Not applicable.
- **What cannot be claimed:** MCL or separate medial/lateral meniscus results from MRNet.
- **Reproducibility artifacts:** Permitted-use rows in docs/data-audit.md.

## Acceptance criteria

- [ ] MRNet row: agreement status (not requested / requested on <date> / approved / declined) and the permitted-use table.
- [ ] Organizer data row: offered yes/no; if yes, label list and terms with source.
- [ ] Each source lists exactly the labels it provides, with a link or file reference.

## Verification

- Reviewer cross-checks label lists against the source documentation.

## Documentation updates

- docs/data-audit.md

## Definition of done

- Rows complete or explicitly 'not offered'.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
