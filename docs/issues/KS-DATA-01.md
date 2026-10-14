<!-- KS-DATA-01 | generated from docs/issues/src/02-data.toml by scripts/backlog.py; edit the source, not this file -->
# KS-DATA-01: Verify RSNA Knee data access and permitted training, hosting, demo and recording uses

| Field | Value |
|---|---|
| Type | decision |
| Priority | P0 |
| Epic | `KS-EPIC-DATA` |
| Workstream | data |
| Recommended owner role | Data/preprocessing (human decision; each data handler accepts rules personally) |
| Status (from state.json) | ready |

## Problem

The RSNA Knee Abnormality Detection rules (read 2026-10-13) permit use of the competition data 'for any purpose … including academic research and education' subject to the MIRA license, but also require participants not to 'redistribute or otherwise provide or make available the Competition Data to any party not participating in the Competition'. Access requires each person to accept the rules before the entry deadline (15 October 2026, 23:59 UTC). Hosting rendered slices publicly, showing them in a recorded video, or sharing a demo machine may count as making data available. The dataset is about 570 GB of DICOM, and only a small subset of training studies carry labels.

## Expected outcome

docs/data-audit.md §1 records, for RSNA: who has accepted the rules (names, not credentials), the MIRA license terms read (link and date), and an explicit yes/no/unclear for: training, local demo to judges, public hosting of rendered slices, recorded video showing slices, and publishing model weights. Unclear items list the question sent to informatics@rsna.org or Kaggle and its status.

## Dependencies

- None — can start now.

- Blocks: `KS-DATA-03` — Audit the accessible dataset(s): studies, series, planes, labels and grouping identifiers
- Blocks: `KS-DEMO-03` — Recorded fallback demonstration within data-use terms

## Scope

- Read the competition Rules and http://rsna.org/mira-license.
- Each team member who will download or view data accepts the rules themselves (human action).
- Answer each permitted-use question with a quoted clause.
- Record download feasibility (570 GB total; whether a subset can be fetched by study).

## Explicit exclusions

- Agents must not accept terms, sign in, or download data on anyone's behalf.
- Do not email organizers without the coordinator's approval of the text.

## Implementation guidance

Quote clauses; do not paraphrase permissions into broader ones. Treat 'unclear' as 'not permitted' for public hosting and recordings until answered. Note that removing identifying tags does not grant redistribution rights.

## Relevant files and modules

- `docs/data-audit.md`
- `docs/decisions.md`

## Contract impact

None directly; feeds KS-DATA-04.

## Scientific requirements

- **Dataset and label provenance:** RSNA Knee Abnormality Detection (Kaggle, 2026), Competition Data subject to Rules §4 and the MIRA license.
- **Evaluation partition:** Not applicable (access decision).
- **Applicable metrics:** Not applicable.
- **What cannot be claimed:** That de-identification permits redistribution; that a local demo or recording is automatically permitted.
- **Reproducibility artifacts:** Dated permitted-use table in docs/data-audit.md.

## Acceptance criteria

- [ ] docs/data-audit.md §1 'Access and permitted use' for RSNA has a row for each of: training, evaluation, local demo, public hosting, recording, weight publication — each 'yes', 'no' or 'unclear' with a quoted clause or pending question.
- [ ] The list of members who personally accepted the rules is recorded (names only).
- [ ] Download feasibility (full or per-study subset) is stated with evidence (command or page reference).

## Verification

- Coordinator and one other member review the table against the rules page.

## Documentation updates

- docs/data-audit.md

## Definition of done

- Table complete; unclear items have an owner and a pending question.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
