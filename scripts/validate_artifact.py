"""Validate a JSON artifact against a contract model.

Usage: python scripts/validate_artifact.py MetricsSnapshot artifacts/metrics/<version>.json
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "contracts")]

from kneescope_contracts import models  # noqa: E402


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    name, path = sys.argv[1], Path(sys.argv[2])
    model = getattr(models, name, None)
    if model is None or model not in models.EXPORTED_MODELS:
        print(f"unknown contract {name}; choose from {[m.__name__ for m in models.EXPORTED_MODELS]}")
        return 2
    model.model_validate_json(path.read_text(encoding="utf-8"))
    print(f"{path}: valid {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
