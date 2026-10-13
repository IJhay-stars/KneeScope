"""Typed access to config/preprocessing.toml and config/model.toml."""

from __future__ import annotations

import hashlib
import tomllib
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"


@dataclass(frozen=True)
class PreprocessingConfig:
    version: str
    status: str
    planes: tuple[str, ...]
    num_slices: int
    height: int
    width: int
    p_low: float
    p_high: float
    render_max_size: int
    render_p_low: float
    render_p_high: float
    sha256: str


@dataclass(frozen=True)
class ModelConfig:
    model_id: str
    model_version: str
    checkpoint_path: str
    checkpoint_sha256: str
    finding_profile: str
    required_planes: tuple[str, ...]
    trained_on: str
    serving_mode: str
    request_timeout_s: float
    cache_dir: str
    fixture_model_id: str
    fixture_model_version: str
    fixture_unsupported: tuple[str, ...]

    @property
    def has_checkpoint(self) -> bool:
        return bool(self.checkpoint_path)


def _read(path: Path) -> tuple[dict, str]:  # type: ignore[type-arg]
    raw = path.read_bytes()
    return tomllib.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()


def load_preprocessing_config(path: Path | None = None) -> PreprocessingConfig:
    data, sha = _read(path or CONFIG_DIR / "preprocessing.toml")
    inp, norm, render = data["input"], data["input"]["normalization"], data["render"]
    if inp["dtype"] != "float32" or inp["layout"] != "S,H,W":
        raise ValueError("contract requires float32 tensors in S,H,W layout")
    return PreprocessingConfig(
        version=data["version"],
        status=data["status"],
        planes=tuple(inp["planes"]),
        num_slices=int(inp["num_slices"]),
        height=int(inp["height"]),
        width=int(inp["width"]),
        p_low=float(norm["p_low"]),
        p_high=float(norm["p_high"]),
        render_max_size=int(render["max_size"]),
        render_p_low=float(render["p_low"]),
        render_p_high=float(render["p_high"]),
        sha256=sha,
    )


def load_model_config(path: Path | None = None) -> ModelConfig:
    data, _ = _read(path or CONFIG_DIR / "model.toml")
    m, s, f = data["model"], data["serving"], data["fixture_model"]
    if s["mode"] not in {"sync", "job"}:
        raise ValueError("serving.mode must be 'sync' or 'job'")
    return ModelConfig(
        model_id=m["model_id"],
        model_version=m["model_version"],
        checkpoint_path=m["checkpoint_path"],
        checkpoint_sha256=m["checkpoint_sha256"],
        finding_profile=m["finding_profile"],
        required_planes=tuple(m["required_planes"]),
        trained_on=m["trained_on"],
        serving_mode=s["mode"],
        request_timeout_s=float(s["request_timeout_s"]),
        cache_dir=s["cache_dir"],
        fixture_model_id=f["model_id"],
        fixture_model_version=f["model_version"],
        fixture_unsupported=tuple(f["unsupported_findings"]),
    )
