<!-- KS-EVAL-06 | generated from docs/issues/src/05-eval.toml by scripts/backlog.py; edit the source, not this file -->
# KS-EVAL-06: Complete the model card from evaluated evidence

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-EVAL` |
| Workstream | evaluation |
| Recommended owner role | Evaluation |
| Status (from state.json) | blocked |

## Problem

docs/model-card.md is a template and contracts/fixtures/model-card.json is a fixture draft. The served card must describe the actual model, data, labels, evaluation, calibration status, explanations and limitations.

## Expected outcome

docs/model-card.md filled; artifacts/model-card/<model_version>.json (ModelCard, status 'published', origin 'dataset') generated from it and served by GET /model-card.

## Dependencies

- Blocked by: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot
- Blocked by: `KS-EVAL-04` — Error analysis: false positives, false negatives and failure cases
- Blocked by: `KS-LABEL-01` — Build the labels file with provenance and explicit unknown handling

- Blocks: `KS-API-05` — Serve real labels, metrics snapshot and model card
- Blocks: `KS-QA-02` — Independent completion review against the evidence-based definition of done

## Scope

- Fill every template section with sources.
- Generate the JSON with scripts/build_model_card.py.
- Limitations include dataset scope, partition type, single-site caveat if applicable, calibration status, explanation caveat.

## Explicit exclusions

- Claims not backed by an artifact.

## Implementation guidance

Every number in the card must link to a snapshot file or experiment entry.

## Relevant files and modules

- `docs/model-card.md`
- `scripts/build_model_card.py`

## Contract impact

Produces ModelCard (contracts).

## Scientific requirements

- **Dataset and label provenance:** Selected dataset.
- **Evaluation partition:** As in KS-EVAL-03.
- **Applicable metrics:** As in KS-EVAL-03.
- **What cannot be claimed:** Anything not in the snapshot or experiment log.
- **Reproducibility artifacts:** Card markdown and JSON with model_version.

## Acceptance criteria

- [ ] No template placeholder text ('TBD', '<…>') remains (scripts/check_docs.py).
- [ ] Generated JSON validates as ModelCard with status 'published'.
- [ ] Every metric in the card matches the KS-EVAL-03 snapshot (script check).

## Verification

- `python scripts/build_model_card.py --check`
- `python scripts/validate_artifact.py ModelCard artifacts/model-card/<model_version>.json`

## Documentation updates

- docs/model-card.md

## Definition of done

- Reviewed by QA role against the snapshot.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
