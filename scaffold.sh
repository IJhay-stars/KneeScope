#!/usr/bin/env bash
# Scaffolds the knee-MRI hackathon monorepo.
# Usage: cd into your empty, cloned repo, then run:  bash scaffold.sh
# Safe to re-run: existing files are never overwritten.
set -euo pipefail

write() { # write <path>  (content on stdin); skips files that already exist
  if [ -e "$1" ]; then echo "skip   $1"; cat >/dev/null; else mkdir -p "$(dirname "$1")"; cat >"$1"; echo "create $1"; fi
}

# ---------------------------------------------------------------- folders
mkdir -p src/kneeml/{data,models,training,inference,eval} \
  src/knee_api/{routers,schemas,services} \
  tests/kneeml tests/knee_api \
  configs docs/contracts docs/adr scripts data models docker .github/workflows

for d in src/kneeml src/kneeml/{data,models,training,inference,eval} \
  src/knee_api src/knee_api/{routers,schemas,services}; do
  [ -e "$d/__init__.py" ] || : >"$d/__init__.py"
done
[ -e data/.gitkeep ] || : >data/.gitkeep
[ -e models/.gitkeep ] || : >models/.gitkeep

# ---------------------------------------------------------------- repo hygiene
write .gitignore <<'EOF'
__pycache__/
*.pyc
.venv/
.env
.mypy_cache/
.ruff_cache/
.pytest_cache/
*.egg-info/
node_modules/
dist/
.DS_Store

# Never commit data, patient images or trained weights
data/*
!data/.gitkeep
models/*
!models/.gitkeep
*.dcm
*.ckpt
*.pt
*.pth
EOF

write .env.example <<'EOF'
APP_ENV=development
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:5173"]
MODEL_PATH=models/baseline.pt
EOF
[ -e .env ] || cp .env.example .env

write README.md <<'EOF'
# Knee MRI Triage (hackathon prototype)

Research prototype. Not for clinical use.

## Layout
- `src/kneeml/`   ML library: data, models, training, inference, eval
- `src/knee_api/` FastAPI service (routers -> services -> kneeml)
- `web/`          React + TypeScript frontend
- `docs/contracts/` interface contracts between workstreams (change = tell every consumer)
- `docs/adr/`     short architecture decision records

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: use Git Bash or WSL
make setup      # installs dev tools and git hooks
make api        # http://localhost:8000/docs
make test
```

## Rules
- Branch per task, PR into `main`, reviewed by someone from another workstream.
- CI must be green. `make lint` and `make test` locally before pushing.
- Never commit data, DICOM files, weights or secrets.
EOF

# ---------------------------------------------------------------- python project + tooling
write pyproject.toml <<'EOF'
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "rsna-knee"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
  "fastapi>=0.110",
  "uvicorn[standard]>=0.29",
  "pydantic>=2",
  "pydantic-settings>=2",
  "numpy",
]

[project.optional-dependencies]
ml = ["torch", "torchvision", "pydicom", "SimpleITK", "scikit-learn", "pandas", "pyyaml"]
dev = ["pytest", "httpx", "ruff", "mypy", "pre-commit"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py310"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.10"
check_untyped_defs = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF

write Makefile <<'EOF'
.PHONY: setup api test lint format up

setup:
	pip install -e ".[dev]" && pre-commit install

api:
	uvicorn knee_api.main:app --reload --port 8000

test:
	pytest

lint:
	ruff check . && ruff format --check . && mypy src

format:
	ruff check --fix . && ruff format .

up:
	docker compose up --build
EOF

write .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
EOF

# ---------------------------------------------------------------- containers
write docker/Dockerfile.api <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
RUN useradd --create-home app
USER app
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')"
CMD ["uvicorn", "knee_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

write docker-compose.yml <<'EOF'
services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./models:/app/models:ro
EOF

# ---------------------------------------------------------------- CI and team process
write .github/workflows/ci.yml <<'EOF'
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: ruff format --check .
      - run: mypy src
      - run: pytest
EOF

write .github/workflows/web.yml <<'EOF'
name: Web CI
on:
  pull_request:
    paths: ["web/**"]

jobs:
  web:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: web
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
          cache-dependency-path: web/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm build
EOF

write .github/CODEOWNERS <<'EOF'
# Replace @handle-mN with real GitHub usernames.
/src/kneeml/data/       @handle-m1
/src/kneeml/models/     @handle-m2
/src/kneeml/training/   @handle-m2
/src/kneeml/eval/       @handle-m4
/src/kneeml/inference/  @handle-m2 @handle-m5
/src/knee_api/          @handle-m5
/web/                   @handle-m6
/docs/contracts/        @handle-m1 @handle-m2 @handle-m4 @handle-m5 @handle-m6
EOF

write .github/pull_request_template.md <<'EOF'
## What and why

## How to test

## Contract change?
- [ ] No
- [ ] Yes: updated `docs/contracts/...` and tagged every consumer

## Checklist
- [ ] Tests added or updated
- [ ] No data, DICOM files, weights or secrets committed
- [ ] CI is green
EOF

# ---------------------------------------------------------------- docs
for c in 01-finding-list 02-labels-file 03-folds-file 04-preprocessed-exam 05-model-io 06-metrics-json 07-openapi; do
  [ -e "docs/contracts/$c.md" ] ||
    printf '# Contract: %s\n\n**Producer:**\n**Consumers:**\n**Status:** draft\n\n## Shape\n\n' "$c" \
      >"docs/contracts/$c.md"
done

write docs/adr/0000-template.md <<'EOF'
# ADR NNNN: Title

**Status:** proposed | accepted | superseded
**Date:**

## Context
What problem or constraint forced a decision?

## Decision
What did we choose?

## Consequences
What gets easier, what gets harder, what did we reject and why?
EOF

write configs/baseline.yaml <<'EOF'
seed: 42
data:
  subset_size: 800
  image_size: 224
model:
  backbone: efficientnet_b0
train:
  epochs: 10
  batch_size: 16
  lr: 0.0003
EOF

# ---------------------------------------------------------------- ML library (stubs that honour the contracts)
write src/kneeml/constants.py <<'EOF'
"""Shared constants. Changing FINDINGS is a contract change (docs/contracts/01-finding-list.md)."""

FINDINGS: list[str] = ["acl", "mcl", "medial_meniscus", "lateral_meniscus"]
MODEL_VERSION = "stub-0"
EOF

write src/kneeml/data/preprocess.py <<'EOF'
"""Shared preprocessing (contract 04). Training, evaluation and the API must all call this."""

import numpy as np


def preprocess_exam(volumes: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """STUB: per-plane intensity normalisation. M1 replaces with the real pipeline."""
    out: dict[str, np.ndarray] = {}
    for plane, volume in volumes.items():
        v = volume.astype("float32")
        out[plane] = (v - v.mean()) / (v.std() + 1e-6)
    return out
EOF

write src/kneeml/inference/predict.py <<'EOF'
"""Model I/O (contract 05). STUB until a real checkpoint exists."""

import zlib

from kneeml.constants import FINDINGS


def predict_exam(exam_id: str) -> dict[str, float]:
    """Return placeholder probabilities (deterministic per exam). NOT real model output."""
    return {name: (zlib.crc32(f"{exam_id}:{name}".encode()) % 1000) / 1000 for name in FINDINGS}
EOF

# ---------------------------------------------------------------- API service (routers -> services -> kneeml)
write src/knee_api/config.py <<'EOF'
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:5173"]
    model_path: str = "models/baseline.pt"


settings = Settings()
EOF

write src/knee_api/schemas/predict.py <<'EOF'
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    exam_id: str


class FindingScore(BaseModel):
    name: str
    probability: float = Field(ge=0, le=1)
    key_slices: list[int] = []


class PredictionResponse(BaseModel):
    exam_id: str
    model_version: str
    findings: list[FindingScore]
    disclaimer: str = "Research prototype. Not for clinical use."
EOF

write src/knee_api/services/prediction.py <<'EOF'
from knee_api.schemas.predict import FindingScore, PredictionResponse
from kneeml.constants import MODEL_VERSION
from kneeml.inference.predict import predict_exam


def run_prediction(exam_id: str) -> PredictionResponse:
    scores = predict_exam(exam_id)
    return PredictionResponse(
        exam_id=exam_id,
        model_version=MODEL_VERSION,
        findings=[FindingScore(name=n, probability=p) for n, p in scores.items()],
    )
EOF

write src/knee_api/routers/health.py <<'EOF'
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready"}
EOF

write src/knee_api/routers/exams.py <<'EOF'
from fastapi import APIRouter

router = APIRouter(tags=["exams"])


@router.get("/exams")
def list_exams() -> list[dict[str, str]]:
    """STUB: replace with the bundled demo exams."""
    return [{"id": "demo-001"}, {"id": "demo-002"}]
EOF

write src/knee_api/routers/predict.py <<'EOF'
from fastapi import APIRouter

from knee_api.schemas.predict import PredictionResponse, PredictRequest
from knee_api.services.prediction import run_prediction

router = APIRouter(tags=["predict"])


@router.post("/predict", response_model=PredictionResponse)
def predict(body: PredictRequest) -> PredictionResponse:
    return run_prediction(body.exam_id)
EOF

write src/knee_api/main.py <<'EOF'
import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from knee_api.config import settings
from knee_api.routers import exams, health, predict

logger = logging.getLogger("knee_api")


def create_app() -> FastAPI:
    logging.basicConfig(
        level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    app = FastAPI(title="Knee MRI Triage API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_id(request: Request, call_next):
        rid = request.headers.get("x-request-id", uuid.uuid4().hex[:12])
        response = await call_next(request)
        response.headers["x-request-id"] = rid
        logger.info("%s %s -> %s [%s]", request.method, request.url.path, response.status_code, rid)
        return response

    app.include_router(health.router)
    app.include_router(exams.router, prefix="/v1")
    app.include_router(predict.router, prefix="/v1")
    return app


app = create_app()
EOF

# ---------------------------------------------------------------- tests
write tests/knee_api/test_api.py <<'EOF'
from fastapi.testclient import TestClient

from knee_api.main import app
from kneeml.constants import FINDINGS

client = TestClient(app)


def test_healthz() -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_predict_returns_every_finding_in_contract_order() -> None:
    r = client.post("/v1/predict", json={"exam_id": "demo-001"})
    assert r.status_code == 200
    body = r.json()
    assert [f["name"] for f in body["findings"]] == FINDINGS
    assert all(0 <= f["probability"] <= 1 for f in body["findings"])
    assert "not for clinical use" in body["disclaimer"].lower()
EOF

write tests/kneeml/test_preprocess.py <<'EOF'
import numpy as np

from kneeml.data.preprocess import preprocess_exam


def test_preprocess_keeps_shape_and_normalises() -> None:
    vol = np.random.default_rng(0).normal(100, 20, size=(8, 16, 16))
    out = preprocess_exam({"sagittal": vol})["sagittal"]
    assert out.shape == vol.shape
    assert abs(float(out.mean())) < 1e-3
EOF

echo
echo "Done. Next:"
echo "  1) python -m venv .venv && source .venv/bin/activate && make setup"
echo "  2) make test && make api      (open http://localhost:8000/docs)"
echo "  3) pnpm create vite web --template react-ts   (frontend, owner M6)"
echo "  4) edit .github/CODEOWNERS with real GitHub usernames"
