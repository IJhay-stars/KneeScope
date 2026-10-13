<!-- KS-DATA-04 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-04: Decide the dataset and supported finding profile

| Field | Value |
|---|---|
| Type | decision |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Coordinator/integrator with Data and Evaluation owners (human decision) |
| Status (from state.json) | blocked |

## Problem

The dataset determines the findings. RSNA may support ACL, MCL, medial and lateral meniscus if enough labelled studies exist; MRNet supports abnormal, ACL tear and meniscal tear; organizer data supports only its labels. Without usable data the product is an interaction prototype.

## Expected outcome

A decision entry selects one dataset and one profile (or the interaction-prototype path) with the audit numbers that justify it; contracts/findings.json marks that profile 'selected' and sets default_profile; findings without enough positives and negatives to evaluate are dropped rather than shown.

## Dependencies

- Blocked by: `KS-DATA-03` — Audit the accessible dataset(s): studies, series, planes, labels and grouping identifiers

- Blocks: `KS-SCOPE-03` — [Conditional] Deliver as an interaction prototype if no usable training data exists
- Blocks: `KS-DATA-05` — Dataset adapter: study listing, plane assignment, series selection and slice ordering
- Blocks: `KS-DATA-08` — Create patient/study-grouped train, validation and test splits with leakage checks
- Blocks: `KS-LABEL-01` — Build the labels file with provenance and explicit unknown handling
- Blocks: `KS-LABEL-02` — [Conditional] Extract labels from radiology reports with negation, uncertainty and provenance
- Blocks: `KS-OPS-05` — [Conditional] Permitted deployment of a hosted demo

## Scope

- Choose dataset and profile using KS-DATA-03 counts and KS-DATA-01/02 permissions.
- Drop any finding whose evaluation partition would lack positives or negatives.
- Decide whether report-label extraction (KS-LABEL-02) is triggered.
- Decide whether KS-SCOPE-03 is triggered.

## Explicit exclusions

- Do not keep four result cards for appearance if labels cannot support them.

## Implementation guidance

State a minimum: e.g. at least N positive and N negative labelled studies per finding in the planned evaluation partition (choose N with the evaluation owner and record it). Adding an organizer profile requires a new profile in findings.json — follow the contract change procedure.

## Relevant files and modules

- `docs/decisions.md`
- `contracts/findings.json`
- `docs/data-audit.md`

## Contract impact

contracts/findings.json: profile status 'selected', default_profile updated; possibly a new profile. Regenerate contracts and notify consumers.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset with version/date and permitted-use reference.
- **Evaluation partition:** Planned evaluation partition sizes per finding (from audit).
- **Applicable metrics:** Counts only.
- **What cannot be claimed:** That dropped findings are detectable; that one dataset's findings transfer to another.
- **Reproducibility artifacts:** Decision entry with audit table excerpt.

## Acceptance criteria

- [ ] docs/decisions.md entry names dataset, version/date, profile, retained findings, dropped findings with reason, and the minimum-count rule.
- [ ] contracts/findings.json default_profile equals the selected profile and its status is 'selected' (or 'interaction_prototype' when KS-SCOPE-03 is triggered).
- [ ] KS-LABEL-02 and KS-SCOPE-03 are marked triggered/not triggered in docs/issue-index.md.
- [ ] python scripts/export_contracts.py --check passes after the change.

## Verification

- `python scripts/export_contracts.py --check`
- `pytest tests/test_contracts.py`

## Documentation updates

- docs/decisions.md
- docs/data-audit.md
- docs/issue-index.md
- contracts/README.md (§1 profile list)

## Definition of done

- Consumers (web, api, ml owners) acknowledged the profile change in the PR.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
