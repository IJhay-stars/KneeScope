"""Load the finding registry (``contracts/findings.json``)."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

from kneescope_contracts.models import FindingDefinition, FindingProfile

REGISTRY_PATH = Path(__file__).resolve().parents[1] / "findings.json"


@cache
def _registry() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    for profile_id, profile in data["profiles"].items():
        unknown = set(profile["findings"]) - set(data["findings"])
        if unknown:
            raise ValueError(f"profile {profile_id} references unknown findings {sorted(unknown)}")
    return data


def registry_version() -> str:
    return str(_registry()["registry_version"])


def default_profile_id() -> str:
    return str(_registry()["default_profile"])


def profile_ids() -> list[str]:
    return list(_registry()["profiles"])


def finding_definition(finding_id: str) -> FindingDefinition:
    entry = _registry()["findings"][finding_id]
    return FindingDefinition(
        finding_id=finding_id,
        display_name=entry["display_name"],
        description=entry["description"],
    )


def load_profile(profile_id: str) -> FindingProfile:
    try:
        profile = _registry()["profiles"][profile_id]
    except KeyError as exc:
        raise KeyError(f"unknown finding profile {profile_id!r}; known: {profile_ids()}") from exc
    return FindingProfile(
        profile_id=profile_id,
        dataset_id=profile["dataset_id"],
        status=profile["status"],
        note=profile["note"],
        findings=[finding_definition(f) for f in profile["findings"]],
    )
