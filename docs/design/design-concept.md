# KneeScope design concept

Status: selected direction recorded 2026-10-13. The canonical specification is
[`DESIGN.md`](../../DESIGN.md); this document records how the direction was chosen.
The interactive concept is [`design-concept.html`](design-concept.html) (open it directly
in a browser; no build step).

## What the concept must solve

KneeScope is a research review workspace, not a marketing product. A researcher spends
most of their time looking at grayscale slices, then reads a short column of model
scores, then checks evidence on a separate evaluation page. The design has to:

1. Keep the image the brightest, calmest, most neutral object on screen.
2. Make provenance impossible to miss: live, cached, and fixture results must look
   different without relying on colour.
3. Keep five finding states distinct: scored, unsupported, not evaluated, unavailable,
   failed. A low score must never look like a failure, and a failure must never look
   like a low score.
4. Read as evidence rather than as a diagnosis. No red/green severity semantics.
5. Be buildable by a small team in React with Tailwind and plain CSS tokens.

The functional reference image in the project plan (dark workspace, teal accents, a
blue-to-red "jet" attention overlay) established the layout. Its palette is rejected:
teal and jet colormaps are blue-family, and the jet map implies precise localisation it
cannot support.

## Three directions

### A. Lightbox & Ledger (selected)

Two materials. Imaging lives on a *lightbox*: a warm-charcoal workspace around a
strictly neutral viewer well. Evidence lives on a *ledger*: the evaluation view and model
card are set as bone-paper documents with a serif display face, ruled tables, and
footnoted limitations. One restrained olive accent marks interaction; clay/rust marks
failure; ochre marks cached results. Fixture data is marked with a hatched stripe and the
word FIXTURE, never a colour alone.

- Imaging readability: high. Dark, neutral surround around the image; no tinted chrome
  touches the viewer well.
- Hierarchy: strong. The material change between lightbox and ledger tells the user
  whether they are looking at an image or at evidence about the model.
- Memorability: high. The paper ledger inside a dark instrument is distinctive without
  decoration.
- Density: comfortable. Compact findings column; generous ledger tables.
- Contrast: all text tokens verified at WCAG AA or better (see `DESIGN.md` §4).
- Effort: moderate. Two surface families share one token set; no imagery, no gradients,
  no custom illustration.

### B. Parchment atelier

An entirely light interface: parchment surfaces, ink-black type, rust accents, an
editorial serif throughout. Beautiful on the evaluation page and in screenshots.

- Imaging readability: poor. A bright surround lowers perceived contrast in dark MRI
  regions and causes glare during long review. Reading rooms are dim for this reason.
- Hierarchy: good on documents, weak around the viewer.
- Memorability: high.
- Effort: low.
- Rejected because the primary task is image review.

### C. Graphite instrument

Monochrome graphite with a single ochre signal colour, monospaced type everywhere,
dense numeric readouts, hairline grid.

- Imaging readability: high.
- Hierarchy: weak. With one signal colour, ochre would have to mean "interactive",
  "cached", and "attention" at once; ochre also reads as a warning, which pushes scores
  toward a severity reading.
- Memorability: moderate; it converges on a generic "terminal dashboard".
- Density: high, tiring for non-specialist reviewers.
- Rejected because it overloads one colour and invites severity interpretation.

## Decision matrix

| Criterion | A. Lightbox & Ledger | B. Parchment atelier | C. Graphite instrument |
|---|---|---|---|
| Imaging readability | Strong | Weak | Strong |
| Visual hierarchy | Strong | Moderate | Weak |
| Memorable identity | Strong | Strong | Moderate |
| Information density | Comfortable | Sparse | Dense |
| Accessible contrast | AA+ verified | AA achievable | AA achievable |
| Implementation effort | Moderate | Low | Low |

Direction A is selected. It is the only one that is strong on the two criteria that
matter most for this product: image readability and a clear separation between images
and evidence.

## What the HTML concept demonstrates

- **Study browser**: table of permitted studies with planes, series counts, origin
  (fixture or dataset) and analysis status, including a study missing its axial series.
- **Review workspace**: plane tabs with a missing-plane state, slice stepping (keyboard,
  slider, buttons), zoom and reset, a simulated "Run analysis" flow, the findings column
  in all five states, the result provenance strip, an "Explanation unavailable" state,
  and a separate "Reveal dataset label" control.
- **Evaluation and model card**: ledger presentation with "Metrics unavailable", an
  explicit undefined-AUC example row, sample-count columns, and limitations.
- **States**: loading, empty, API error, missing series, failed analysis, and an
  unsupported finding when the finding scope changes from RSNA-4 to MRNet-3.

All imagery is a synthetic grayscale test pattern, not anatomy. All study identifiers,
scores, and labels are fixtures and are labelled as such on screen. The analysis run is
simulated in the browser and is labelled as simulated.

## Verification of the concept

Recorded in [`docs/issue-index.md`](../issue-index.md) under "Scaffold verification" and
in the final scaffold report: the HTML was opened in a browser and screenshotted at
desktop and narrow widths, and colour tokens were checked programmatically for contrast
and for hue (no token falls in the blue or purple hue range).
