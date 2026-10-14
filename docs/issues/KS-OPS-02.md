<!-- KS-OPS-02 | generated from docs/issues/src/08-quality.toml by scripts/backlog.py; edit the source, not this file -->
# KS-OPS-02: Reproducible local container setup for API and web

| Field | Value |
|---|---|
| Type | task |
| Priority | P1 |
| Epic | `KS-EPIC-QUALITY` |
| Workstream | operations |
| Recommended owner role | Backend/serving |
| Status (from state.json) | blocked |

## Problem

The plan requires one reproducible local or container setup. Judges or teammates must be able to run the app without the authors' machines, with data and checkpoints mounted rather than baked in.

## Expected outcome

Dockerfile (API, CPU torch), web static build served by the API or a small static server, docker-compose.yml with read-only mounts for manifest, data subset, checkpoint and cache; fixture mode works with no mounts.

## Dependencies

- Blocked by: `KS-API-02` — Live inference through shared preprocessing in POST /predictions

- Blocks: `KS-OPS-05` — [Conditional] Permitted deployment of a hosted demo
- Blocks: `KS-DOC-01` — Reproducible README: a teammate sets up and runs inference from a clean clone

## Scope

- Multi-stage builds pinned to lockfiles.
- Compose profiles: fixture (no mounts) and model (mounts).
- Healthcheck on /healthz.
- Image contains no data or checkpoints (verified).

## Explicit exclusions

- Kubernetes, cloud registries, GPU images.

## Implementation guidance

Use `uv sync --frozen` and `pnpm install --frozen-lockfile`. Document image size.

## Relevant files and modules

- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `README.md`

## Contract impact

None.

## Acceptance criteria

- [ ] `docker compose --profile fixture up` serves the web app and /healthz returns mode 'fixture' on a clean clone.
- [ ] `docker compose --profile model up` with mounts returns model_loaded true.
- [ ] `docker run --rm <image> find / -name '*.dcm' -o -name '*.pt'` finds nothing.
- [ ] README documents both profiles.

## Verification

- `docker compose --profile fixture up -d && curl -fs localhost:8000/healthz`
- `docker compose --profile model up -d && curl -fs localhost:8000/healthz`

## Documentation updates

- README.md
- docs/architecture.md (deployment)

## Definition of done

- A teammate ran it from a clean clone (KS-DOC-01 evidence).
- Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.
- Verification commands pass locally and in CI where CI covers them.
- Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.
- PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.
- docs/issues/state.json and docs/issue-index.md updated (status, links).
