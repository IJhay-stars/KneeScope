"""Synthetic phantom adapter for development fixtures.

Produces geometric test volumes (nested spheres plus a grey step wedge). They are not
anatomy and must always be labelled "Synthetic test pattern - not an MRI".
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

import numpy as np

from kneescope_ml.adapters.base import SeriesRef
from kneescope_ml.types import SeriesVolume

FIXTURE_DIR = Path(__file__).resolve().parents[3] / "contracts" / "fixtures"
PHANTOM_SIZE = 256


@cache
def _studies() -> dict[str, dict]:  # type: ignore[type-arg]
    data = json.loads((FIXTURE_DIR / "studies.json").read_text(encoding="utf-8"))
    return {s["study_id"]: s for s in data["studies"]}


def phantom_volume(n_slices: int, plane_offset: float, size: int = PHANTOM_SIZE) -> np.ndarray:
    """Nested-sphere phantom; cross-section radius varies with slice position."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    cy, cx, radius = size * 0.46, size * 0.5, size * 0.36
    vol = np.full((n_slices, size, size), 18.0, dtype=np.float32)
    for k in range(n_slices):
        z = (k + 0.5) / n_slices * 2 - 1
        r = radius * np.sqrt(max(0.0, 1 - z * z))
        d = np.hypot(yy - cy, xx - cx)
        vol[k][d <= r] = 150.0
        vol[k][d <= r * 0.62] = 92.0
        d2 = np.hypot(yy - (cy - r * 0.15), xx - (cx - r * plane_offset))
        vol[k][d2 <= r * 0.2] = 210.0
        wedge_top, wedge_h = int(size * 0.88), int(size * 0.06)
        for i in range(8):
            x0 = int(size * 0.1 + i * size * 0.1)
            vol[k, wedge_top : wedge_top + wedge_h, x0 : x0 + int(size * 0.1)] = 16 + i * 34
    return vol


class FixtureAdapter:
    dataset_id = "fixture"

    def list_studies(self) -> list[str]:
        return list(_studies())

    def list_series(self, study_id: str) -> list[SeriesRef]:
        study = _studies()[study_id]
        return [
            SeriesRef(
                study_id=study_id,
                series_id=s["series_id"],
                plane=s["plane"],
                num_slices=s["num_slices"],
                slice_order=s["slice_order"],
                description=s.get("description"),
                fluid_sensitive=s.get("fluid_sensitive"),
                fat_suppressed=s.get("fat_suppressed"),
            )
            for s in study["series"]
        ]

    def load_series(self, study_id: str, series_id: str) -> SeriesVolume:
        ref = next(s for s in self.list_series(study_id) if s.series_id == series_id)
        offset = {"sagittal": 0.2, "coronal": 0.38, "axial": 0.56}.get(ref.plane or "", 0.0)
        return SeriesVolume(
            study_id=study_id,
            series_id=series_id,
            plane=ref.plane,
            pixels=phantom_volume(ref.num_slices, offset),
            slice_order=ref.slice_order,
            description=ref.description,
        )

    def select_series(self, study_id: str) -> dict[str, SeriesRef]:
        chosen: dict[str, SeriesRef] = {}
        for ref in self.list_series(study_id):
            if ref.plane and ref.plane not in chosen:
                chosen[ref.plane] = ref
        return chosen
