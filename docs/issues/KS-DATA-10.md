<!-- KS-DATA-10 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-10: Select permitted demo studies and build the study manifest

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing with Evaluation |
| Status (from state.json) | blocked |

## Problem

The app shows a small set of bundled studies (PRD: 3–5). They must be permitted for demonstration, come from the evaluation partition (not training), and cover a correct case, an error/missing-series case and a limitation case.

## Expected outcome

scripts/build_manifest.py writes artifacts/manifest/studies.json (untracked if data terms require) listing 3–5 studies with series metadata in StudyDetail shape; selection rationale recorded without patient information.

## Dependencies

- Blocked by: `KS-DATA-07` — Freeze shared preprocessing v1 with visual inspection evidence
- Blocked by: `KS-DATA-08` — Create patient/study-grouped train, validation and test splits with leakage checks

- Blocks: `KS-EVAL-07` — Precompute cached predictions for the demo studies with full provenance
- Blocks: `KS-DEMO-01` — Select demo cases: a correct case, an error case and a limitation

## Scope

- Pick studies from validation/test partition only.
- Include at least one study with a missing plane.
- Manifest validates against StudyDetail.
- Record permission basis for showing them.

## Explicit exclusions

- No studies from the training partition.
- No public hosting of the manifest images unless permitted (KS-OPS-05).

## Implementation guidance

Final choice of demo cases depends on evaluation results (KS-DEMO-01); this issue provides the candidate pool and the manifest tooling.

## Relevant files and modules

- `scripts/build_manifest.py`
- `docs/data-audit.md`
- `tests/ml/test_manifest.py`

## Contract impact

Produces StudyDetail records; no schema change.

## Acceptance criteria

- [ ] Manifest validates against StudyDetail (test).
- [ ] Every manifest study is in validation or test partition (test against split file).
- [ ] At least one manifest study has a missing plane.
- [ ] Permission basis cites the KS-DATA-01/02 table row.

## Verification

- `python scripts/build_manifest.py --out artifacts/manifest/studies.json`
- `pytest tests/ml/test_manifest.py`

## Documentation updates

- docs/data-audit.md §6 'Demo studies'

## Definition of done

- Evaluation owner confirms none are training studies.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
