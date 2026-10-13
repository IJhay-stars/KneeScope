<!-- KS-OPT-01 | generated from docs/issues/src/10-optional.toml by scripts/backlog.py; edit the source, not this file -->
# KS-OPT-01: [Optional] Upload support for user-supplied studies

| Field | Value |
|---|---|
| Type | optional |
| Priority | P2 |
| Epic | `KS-EPIC-API` |
| Workstream | backend |
| Recommended owner role | Backend/serving with Coordinator approval |
| Status (from state.json) | optional-blocked |

## Problem

The plan lists general upload as 'add after the core works'. Uploads raise privacy, permission and robustness questions.

## Expected outcome

Local-only upload of a DICOM study (zip) processed through the same adapter rules, never persisted beyond the session, never logged, rejected if not de-identified per a documented check.

## Dependencies

- Blocked by: `KS-API-02` — Live inference through shared preprocessing in POST /predictions
- Blocked by: `KS-OPS-01` — Restricted-asset protection: data, checkpoints, logs and repository guards

- None.

## Scope

- Size and type limits.
- Temporary storage with deletion.
- Same preprocessing and error mapping.

## Explicit exclusions

- Public hosting with upload enabled.
- PHI handling claims.

## Implementation guidance

Requires a decision entry approving it after the core is complete.

## Relevant files and modules

- `api/kneescope_api/upload.py`
- `web/src/pages/UploadPage.tsx`
- `tests/api/test_upload.py`

## Contract impact

Adds an upload endpoint and response (minor version).

## Acceptance criteria

- [ ] Upload of a synthetic DICOM zip yields a temporary study that predicts via the live path (test).
- [ ] Temporary files are deleted after the session or 1 hour (test).
- [ ] Upload of a file containing PatientName is rejected (test).

## Verification

- `pytest tests/api/test_upload.py`

## Documentation updates

- docs/security.md
- contracts/README.md

## Definition of done

- Decision entry approving the feature exists.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
