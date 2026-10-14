"""Regenerate contract artifacts from the Pydantic models and the FastAPI app.

Writes:
  contracts/schema/<Model>.schema.json   one JSON Schema per exported model
  contracts/openapi.json                 OpenAPI document of the API
  contracts/examples/*.json              example responses produced in fixture mode

Usage:
  python scripts/export_contracts.py          # write files
  python scripts/export_contracts.py --check  # exit 1 if any file would change (CI)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("KNEESCOPE_MODE", "fixture")
os.environ.setdefault("KNEESCOPE_FINDING_PROFILE", "interaction_prototype")

from fastapi.testclient import TestClient

from kneescope_api.main import create_app
from kneescope_contracts.models import EXPORTED_MODELS

ROOT = Path(__file__).resolve().parents[1]
VOLATILE = {"served_at", "request_id"}


def dump(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def scrub(data: object) -> object:
    """Replace per-request values so examples are stable."""
    if isinstance(data, dict):
        return {k: ("<volatile>" if k in VOLATILE else scrub(v)) for k, v in data.items()}
    if isinstance(data, list):
        return [scrub(v) for v in data]
    return data


def build() -> dict[Path, str]:
    out: dict[Path, str] = {}
    for model in EXPORTED_MODELS:
        out[ROOT / "contracts" / "schema" / f"{model.__name__}.schema.json"] = dump(
            model.model_json_schema(mode="serialization")
        )
    app = create_app()
    out[ROOT / "contracts" / "openapi.json"] = dump(app.openapi())
    client = TestClient(app)
    examples = {
        "health": client.get("/healthz"),
        "findings": client.get("/findings"),
        "studies": client.get("/studies"),
        "study-detail": client.get("/studies/fx-study-001"),
        "prediction-fixture": client.post("/predictions", json={"study_id": "fx-study-001"}),
        "prediction-missing-plane": client.post("/predictions", json={"study_id": "fx-study-004"}),
        "error-preprocessing-failed": client.post("/predictions", json={"study_id": "fx-study-003"}),
        "error-study-not-found": client.get("/studies/does-not-exist"),
        "explanation-available": client.get(
            "/studies/fx-study-001/explanations/acl",
            params={"prediction_id": "fx-pred-fx-study-001-interaction_prototype"},
        ),
        "explanation-unavailable": client.get(
            "/studies/fx-study-001/explanations/mcl",
            params={"prediction_id": "fx-pred-fx-study-001-interaction_prototype"},
        ),
        "labels": client.get("/studies/fx-study-001/labels"),
        "metrics-unavailable": client.get("/metrics"),
        "model-card": client.get("/model-card"),
    }
    for name, resp in examples.items():
        out[ROOT / "contracts" / "examples" / f"{name}.json"] = dump(
            {"status": resp.status_code, "body": scrub(resp.json())}
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, text in build().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            stale.append(path.relative_to(ROOT))
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
    if args.check and stale:
        print("Contract artifacts are stale; run python scripts/export_contracts.py:")
        for p in stale:
            print(f"  {p}")
        return 1
    print(f"contract artifacts {'up to date' if not stale else 'written: ' + str(len(stale))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
