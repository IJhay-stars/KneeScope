<!-- KS-MODEL-05 | generated from docs/issues/src/04-model.toml by scripts/backlog.py; edit the source, not this file -->
# KS-MODEL-05: Package the checkpoint for serving with hash verification and a Predictor implementation

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-MODEL` |
| Workstream | modelling |
| Recommended owner role | Modelling with Backend reviewer |
| Status (from state.json) | blocked |

## Problem

kneescope_ml.inference.load_predictor is a placeholder. Serving needs a CPU-capable Predictor that loads the checkpoint, verifies its SHA-256 against config/model.toml, and exposes model_id, model_version and supported_findings.

## Expected outcome

load_predictor returns a working Predictor; config/model.toml is filled for the chosen checkpoint (path outside git); a tiny synthetic checkpoint is generated in tests to exercise the path in CI.

## Dependencies

- Blocked by: `KS-MODEL-03` — Train the baseline model on the selected dataset

- Blocks: `KS-API-02` — Live inference through shared preprocessing in POST /predictions
- Blocks: `KS-DOC-01` — Reproducible README: a teammate sets up and runs inference from a clean clone

## Scope

- Checkpoint format (state_dict + metadata JSON).
- SHA-256 verification; mismatch → ModelNotAvailableError.
- CPU inference, eval mode, no grad.
- Test with a generated tiny checkpoint.

## Explicit exclusions

- GPU hosting.
- Committing checkpoint files.

## Implementation guidance

Model weights may be subject to the dataset terms (e.g. RSNA winners' licensing does not apply to us, but data-derived weights' distribution should be checked under KS-DATA-01). Store under artifacts/checkpoints/ (ignored).

## Relevant files and modules

- `ml/kneescope_ml/inference.py`
- `config/model.toml`
- `tests/ml/test_inference.py`

## Contract impact

ModelInfo values in every live/cached prediction.

## Acceptance criteria

- [ ] Test: generated tiny checkpoint loads and predict() returns scores in [0,1] for exactly the supported findings.
- [ ] Test: a tampered checkpoint (one byte changed) raises ModelNotAvailableError.
- [ ] config/model.toml has non-empty model_version, checkpoint_sha256, finding_profile matching the selected profile.

## Verification

- `uv sync --extra ml && pytest tests/ml/test_inference.py`

## Documentation updates

- README.md 'Model artifacts' section
- docs/model-card.md versions

## Definition of done

- Weight distribution permission noted in docs/data-audit.md §1.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
