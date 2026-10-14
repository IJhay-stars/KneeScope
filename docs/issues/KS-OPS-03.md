<!-- KS-OPS-03 | generated from docs/issues/src/08-quality.toml by scripts/backlog.py; edit the source, not this file -->
# KS-OPS-03: Measure inference latency, peak memory and slice-serving latency

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-QUALITY` |
| Workstream | operations |
| Recommended owner role | Backend/serving with Evaluation reviewer |
| Status (from state.json) | blocked |

## Problem

Whether synchronous inference is sufficient must be measured, not assumed. The metrics page also reports latency and peak memory on stated hardware.

## Expected outcome

scripts/benchmark_inference.py measures p50/p95 latency and peak RSS over ≥20 runs per study on the target demo hardware, plus slice endpoint latency; results stored as InferenceMeasurement and a decision on sync vs job-and-poll.

## Dependencies

- Blocked by: `KS-API-02` — Live inference through shared preprocessing in POST /predictions

- Blocks: `KS-OPS-04` — [Conditional] Minimal job-and-poll inference flow

## Scope

- Benchmark live path end to end (HTTP) and model-only.
- Record hardware (CPU model, RAM, GPU none/yes).
- Compare p95 with serving.request_timeout_s.
- Decision entry.

## Explicit exclusions

- Optimisation work unless p95 exceeds the limit.

## Implementation guidance

Warm-up runs excluded and stated. Same checkpoint and preprocessing as served.

## Relevant files and modules

- `scripts/benchmark_inference.py`
- `docs/decisions.md`
- `artifacts/metrics/ (inference section)`

## Contract impact

Fills MetricsSnapshot.inference.

## Scientific requirements

- **Dataset and label provenance:** Demo manifest studies.
- **Evaluation partition:** Not applicable (operational).
- **Applicable metrics:** Latency p50/p95, peak memory.
- **What cannot be claimed:** Performance on other hardware.
- **Reproducibility artifacts:** Benchmark JSON with hardware string and git SHA.

## Acceptance criteria

- [ ] Benchmark output includes n_runs ≥ 20, p50, p95, peak memory MB, hardware string.
- [ ] Decision entry: sync kept or KS-OPS-04 triggered, citing p95 vs request_timeout_s.
- [ ] InferenceMeasurement validates and appears on the evaluation page.

## Verification

- `python scripts/benchmark_inference.py --runs 20 --url http://localhost:8000`

## Documentation updates

- docs/decisions.md
- docs/model-card.md

## Definition of done

- KS-OPS-04 marked triggered or not triggered in docs/issue-index.md.
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
