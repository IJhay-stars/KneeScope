<!-- KS-MODEL-03 | generated from docs/issues/src/04-model.toml by scripts/backlog.py; edit the source, not this file -->
# KS-MODEL-03: Train the baseline model on the selected dataset

| Field | Value |
|---|---|
| Type | task |
| Priority | P0 |
| Epic | `KS-EPIC-MODEL` |
| Workstream | modelling |
| Recommended owner role | Modelling |
| Status (from state.json) | blocked |

## Problem

The product needs one honest baseline: frozen pretrained encoder plus trained heads first, documented slice sampling, masked loss, and class weighting only if imbalance justifies it.

## Expected outcome

One run on the training partition, model selection on validation only, checkpoint saved outside git with SHA-256, config and metadata recorded, validation metrics logged.

## Dependencies

- Blocked by: `KS-MODEL-02` — Training pipeline with config, seeding, checkpointing and experiment provenance
- Blocked by: `KS-DATA-09` — Preprocessed tensor cache and training/evaluation data loaders
- Blocked by: `KS-LABEL-01` — Build the labels file with provenance and explicit unknown handling
- Blocked by: `KS-DATA-08` — Create patient/study-grouped train, validation and test splits with leakage checks

- Blocks: `KS-LABEL-03` — Influential-slice explanations aligned to series slice coordinates
- Blocks: `KS-MODEL-04` — [Conditional] One improvement round (fine-tuning or adjacent-slice input)
- Blocks: `KS-MODEL-05` — Package the checkpoint for serving with hash verification and a Predictor implementation
- Blocks: `KS-EVAL-02` — Select per-finding operating thresholds on the validation partition
- Blocks: `KS-EVAL-03` — Held-out evaluation run and published metrics snapshot

## Scope

- Frozen-encoder baseline with trained pooling and heads.
- Early stopping/selection on validation loss or validation macro AUC (declare which).
- Record compute used (hardware, wall time).
- Log validation metrics through kneescope_ml.evaluation.

## Explicit exclusions

- Fine-tuning (KS-MODEL-04, conditional).
- Any use of the test partition.

## Implementation guidance

If compute is limited (e.g. Kaggle/Colab GPU quotas), reduce resolution or slice count and record it — do not assume a paid GPU subscription. Expect modest results; report them as they are.

## Relevant files and modules

- `config/train.toml`
- `docs/experiments.md`
- `artifacts/runs/ (untracked)`

## Contract impact

Defines supported_findings and model_version for config/model.toml.

## Scientific requirements

- **Dataset and label provenance:** Selected dataset, cached tensors at frozen preprocessing version.
- **Evaluation partition:** Train for fitting; validation for selection.
- **Applicable metrics:** Validation per-finding ROC AUC, PR AUC, counts (via KS-EVAL-01).
- **What cannot be claimed:** Test performance; calibration; clinical utility.
- **Reproducibility artifacts:** Checkpoint (untracked) + SHA-256, config, metadata, validation metrics JSON.

## Acceptance criteria

- [ ] docs/experiments.md lists the run with run_id, seed, git SHA, preprocessing version, split hash, hardware, wall time, checkpoint SHA-256.
- [ ] Validation metrics JSON exists for the run and validates against MetricsSnapshot with partition 'validation'.
- [ ] The test partition was not loaded during training or selection (data loader logs show only train/validation).

## Verification

- `python scripts/train.py --config config/train.toml`
- `python scripts/validate_artifact.py MetricsSnapshot artifacts/runs/<run_id>/metrics_validation.json`

## Documentation updates

- docs/experiments.md
- docs/model-card.md (training section)

## Definition of done

- Evaluation owner confirms the run used the agreed partitions.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
