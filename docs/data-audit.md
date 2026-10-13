# Data audit — TEMPLATE

> **Status: template, partially pre-filled from public pages only.** No data has been
> downloaded or inspected. Sections marked `<…>` are filled by KS-DATA-01/02/03/08/10.
> Never put study UIDs, patient information or report text in this file — counts only.

## 1. Access and permitted use

Facts below were read from the public Kaggle competition pages on 2026-10-13 (Overview,
Data, Rules). They are not legal advice; quote clauses when filling the table.

**RSNA Knee Abnormality Detection (Kaggle, 2026)** — public facts:
- 12 per-study binary labels: ACL, MCL, Medial Meniscus, Lateral Meniscus, Medial OA,
  Lateral OA, PF OA, Effusion, Synovitis, Baker's, Contusion, Fracture.
- "Only a small subset of training studies carry per-condition labels"; original
  multilingual report text is provided for training studies; test labels are hidden.
- DICOM series organised `train_series/<StudyInstanceUID>/<SeriesInstanceUID>/`;
  `train_series.csv` gives `Anatomical_Plane`, `Fluid_Sensitive`, `Fat_Suppression`.
  Series typically 20–45 slices (median 30). Mixed transfer syntaxes (Explicit/Implicit
  VR, JPEG Lossless, JPEG 2000). Metadata stripped to 86 allow-listed tags.
- ~570 GB, ~820k files.
- Rules §4a: data may be used "for any purpose, whether commercial or non-commercial …
  and for academic research and education", subject to the MIRA license
  (http://rsna.org/mira-license). Rules §4b: participants must not "transmit, duplicate,
  publish, redistribute or otherwise provide or make available the Competition Data to
  any party not participating in the Competition".
- Entry deadline (rules acceptance): 15 October 2026, 23:59 UTC. Final submission
  deadline 22 October 2026 (not relevant to KneeScope, which is not a submission).

| Use | RSNA | MRNet | Organizer data |
|---|---|---|---|
| Training | `<yes/no/unclear + clause>` | `<…>` | `<…>` |
| Evaluation | `<…>` | `<…>` | `<…>` |
| Local demo to judges | `<…>` | `<…>` | `<…>` |
| Public hosting of rendered slices | `<…>` (see §4b) | `<…>` | `<…>` |
| Recorded video showing slices | `<…>` | `<…>` | `<…>` |
| Publishing model weights | `<…>` | `<…>` | `<…>` |
| Members who accepted terms (names only) | `<…>` | `<…>` | `<…>` |
| Agreement / access status | `<…>` | `<not requested / requested / approved>` | `<offered?>` |

Unclear items default to **not permitted** for hosting and recordings until answered.

## 2. Dataset inventory (KS-DATA-03)
| Item | Value |
|---|---|
| Dataset / version / download date | `<…>` |
| Studies (total / labelled) | `<…>` |
| Series per study (median, range) | `<…>` |
| Slices per series (median, range) | `<…>` |
| Transfer syntaxes (counts) | `<…>` |
| Unreadable/corrupt files | `<…>` |
| Disk size of subset used | `<…>` |

## 3. Labels (KS-DATA-03, KS-LABEL-01)
| Finding | Positive | Negative | Unknown/missing | Not labelled | Source |
|---|---|---|---|---|---|
| `<…>` | | | | | |

## 4. Planes and series
| Plane | Studies with ≥1 series | Studies missing | Series selection rule |
|---|---|---|---|
| Sagittal | | | `<…>` |
| Coronal | | | |
| Axial | | | |

## 5. Grouping and splits (KS-DATA-08)
- Patient identifier available: `<field name or "not available">`
- Site identifier available: `<…>`
- Split method, seed, split hash: `<…>`

| Partition | Studies | Per-finding n+ / n− / unknown |
|---|---|---|
| Train | | |
| Validation | | |
| Test (if any) | | |

## 6. Demo studies (KS-DATA-10)
Manifest IDs only, partition of each, role (correct / error / limitation), permission
basis (row in §1).
