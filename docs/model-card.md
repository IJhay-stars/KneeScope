# Model card — TEMPLATE

> **Status: template.** No model has been trained. Every section below must be filled
> from evidence (`KS-EVAL-06`). Until then the API serves the fixture draft in
> `contracts/fixtures/model-card.json` and `GET /metrics` is `unavailable`.
> Delete this notice when the card is published.

Fill rules: every number links to an artifact (metrics snapshot, experiment entry). Use
"model score" unless calibration is demonstrated. Never "accuracy" for AUC.

## 1. Model details
- Model ID / version: `<model_version>`
- Checkpoint SHA-256: `<sha256>`
- Architecture: `<backbone, pretrained weights source and licence, pooling, plane fusion, heads>`
- Preprocessing version: `<prep version + config SHA-256>`
- Training run: `<run_id, git SHA, seed, hardware, wall time>`
- Finding profile: `<profile id>` → findings: `<list>`

## 2. Intended use
Research and teaching review of permitted knee MRI studies. Not for diagnosis, triage or
treatment.

## 3. Out-of-scope use
Clinical use; studies outside the permitted dataset; other datasets or sites without
evaluation; any claim of clinical benefit.

## 4. Data
- Dataset, version/date, permitted-use basis: `<link to docs/data-audit.md §1>`
- Studies used per partition: `<train / validation / test counts>`
- Planes and series selection rule: `<rule>`
- Known dataset limitations: `<sites, scanners, languages, labelled subset size>`

## 5. Labels and provenance
| Finding | Label source | Positives | Negatives | Unknown | Notes |
|---|---|---|---|---|---|
| `<finding>` | `<expert_annotation / dataset_provided / report_extracted vX>` | | | | |

## 6. Training
Loss (masked BCE; weighting if any and why), sampling, augmentation, epochs, selection
criterion (validation only).

## 7. Evaluation
- Partition: `<validation | held-out test>` — and why
- Split method and grouping unit: `<patient | study>`
- Snapshot: `<artifacts/metrics/<model_version>.json>`

| Finding | n+ | n− | n unknown | ROC AUC | PR AUC | Prevalence | Sens @ thr | Spec @ thr |
|---|---|---|---|---|---|---|---|---|
| `<finding>` | | | | `<value or "Undefined — one class only">` | | | | |

Macro ROC AUC: `<value>` over `<included findings>`; excluded: `<findings and reasons>`.
Comparator (KS-MODEL-01) on the same partition: `<table or link>`.
Inference: p50 `<ms>`, p95 `<ms>`, peak memory `<MB>` on `<hardware>`.

## 8. Calibration
`<Not assessed — scores are uncalibrated model scores>` or the KS-EVAL-05 result.

## 9. Explanations
`<Influential slices / model attention method>`. Shows what influenced a score; does not
localise an injury. Alignment tests: `<link>`.

## 10. Failure analysis
Summary of KS-EVAL-04 with categories and counts; link to `docs/error-analysis.md`.

## 11. Limitations
1. Scores are uncalibrated unless §8 says otherwise.
2. AUC measures ranking, not accuracy.
3. Explanations do not localise injuries.
4. Not validated on other datasets or sites.
5. `<partition caveat, sample-size caveat, label-noise caveat>`

## 12. Versions
Contract `<SCHEMA_VERSION>` · findings registry `<version>` · preprocessing `<version>` ·
model `<version>` · card updated `<date>`.
