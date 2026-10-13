"""Adapter interface shared by all datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from kneescope_ml.types import SeriesVolume


@dataclass(frozen=True)
class SeriesRef:
    study_id: str
    series_id: str
    plane: str | None
    num_slices: int
    slice_order: str
    description: str | None = None
    fluid_sensitive: bool | None = None
    fat_suppressed: bool | None = None


class DatasetAdapter(Protocol):
    dataset_id: str

    def list_studies(self) -> list[str]: ...

    def list_series(self, study_id: str) -> list[SeriesRef]: ...

    def load_series(self, study_id: str, series_id: str) -> SeriesVolume: ...

    def select_series(self, study_id: str) -> dict[str, SeriesRef]:
        """Pick at most one series per plane for model input (documented rule)."""
        ...
