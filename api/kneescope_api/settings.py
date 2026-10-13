"""Runtime settings from environment variables (see .env.example)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

from kneescope_contracts.findings import default_profile_id


@dataclass(frozen=True)
class Settings:
    mode: Literal["fixture", "model"]
    finding_profile: str
    cors_origins: tuple[str, ...]
    log_level: str


def load_settings() -> Settings:
    mode = os.environ.get("KNEESCOPE_MODE", "fixture")
    if mode not in ("fixture", "model"):
        raise ValueError("KNEESCOPE_MODE must be 'fixture' or 'model'")
    origins = os.environ.get("KNEESCOPE_CORS_ORIGINS", "http://localhost:5173")
    return Settings(
        mode=mode,  # type: ignore[arg-type]
        finding_profile=os.environ.get("KNEESCOPE_FINDING_PROFILE", default_profile_id()),
        cors_origins=tuple(o.strip() for o in origins.split(",") if o.strip()),
        log_level=os.environ.get("KNEESCOPE_LOG_LEVEL", "info"),
    )
