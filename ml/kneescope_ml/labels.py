"""Dataset label access for evaluation and the "Reveal dataset label" view only.

Labels are never an inference input. Do not import this module from
``kneescope_ml.inference``, ``kneescope_ml.preprocess`` or the API prediction path.
"""

from __future__ import annotations

import json
from pathlib import Path

LABEL_STATES = ("positive", "negative", "unknown", "not_labeled")


def load_fixture_labels(path: Path) -> dict[str, dict[str, dict[str, str | None]]]:
    """Return {study_id: {finding_id: {state, provenance, source_ref}}} from a fixture."""
    data = json.loads(path.read_text(encoding="utf-8"))
    for study in data["studies"].values():
        for label in study.values():
            if label["state"] not in LABEL_STATES:
                raise ValueError(f"invalid label state {label['state']!r}")
    return data["studies"]  # type: ignore[no-any-return]
