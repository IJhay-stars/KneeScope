"""The single shared preprocessing implementation (contract: contracts/README.md).

Training, evaluation, prediction caching and the API all call ``preprocess_study``.
Do not copy or reimplement this logic elsewhere; change it here, bump
``config/preprocessing.toml`` ``version``, and invalidate caches.

Status: functional placeholder. Slice sampling, resizing, normalisation and masking
work on in-memory volumes. DICOM ordering and orientation handling belong to the dataset
adapters and are tracked in the backlog (KS-DATA-05, KS-DATA-06).
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from kneescope_ml.config import PreprocessingConfig
from kneescope_ml.types import FloatArray, PlaneTensor, PreprocessedStudy, SeriesVolume


class PreprocessingError(ValueError):
    """Input could not be preprocessed. Message is safe to show to a reviewer."""


def sample_slice_indices(n_slices: int, target: int) -> np.ndarray:
    """Evenly spaced, centred indices into an ordered series; never repeats a slice.

    Returns at most ``target`` indices. Shorter series are padded later and masked.
    """
    if n_slices < 1:
        raise PreprocessingError("series has no slices")
    if n_slices <= target:
        return np.arange(n_slices, dtype=np.int64)
    step = n_slices / target
    return np.floor(step * (np.arange(target) + 0.5)).astype(np.int64)


def normalise(volume: FloatArray, p_low: float, p_high: float) -> FloatArray:
    """Clip to per-series percentiles, then z-score. Constant volumes map to zeros."""
    if not np.isfinite(volume).all():
        raise PreprocessingError("series contains non-finite intensities")
    lo, hi = np.percentile(volume, [p_low, p_high])
    clipped = np.clip(volume, lo, hi).astype(np.float32)
    std = float(clipped.std())
    if std < 1e-6:
        return np.zeros_like(clipped, dtype=np.float32)
    return ((clipped - float(clipped.mean())) / std).astype(np.float32)


def resize_slice(img: FloatArray, height: int, width: int, pad_value: float) -> FloatArray:
    """Bilinear resize preserving aspect ratio, centred and padded to (height, width)."""
    rows, cols = img.shape
    scale = min(height / rows, width / cols)
    new_h, new_w = max(1, round(rows * scale)), max(1, round(cols * scale))
    resized = np.asarray(
        Image.fromarray(img.astype(np.float32), mode="F").resize((new_w, new_h), Image.Resampling.BILINEAR),
        dtype=np.float32,
    )
    out = np.full((height, width), pad_value, dtype=np.float32)
    top, left = (height - new_h) // 2, (width - new_w) // 2
    out[top : top + new_h, left : left + new_w] = resized
    return out


def preprocess_series(series: SeriesVolume, cfg: PreprocessingConfig) -> PlaneTensor:
    pixels = np.asarray(series.pixels, dtype=np.float32)
    if pixels.ndim != 3:
        raise PreprocessingError(f"series {series.series_id} must be 3-D (slices, rows, cols)")
    idx = sample_slice_indices(pixels.shape[0], cfg.num_slices)
    norm = normalise(pixels[idx], cfg.p_low, cfg.p_high)
    pad = float(norm.min()) if norm.size else 0.0
    volume = np.full((cfg.num_slices, cfg.height, cfg.width), pad, dtype=np.float32)
    mask = np.zeros(cfg.num_slices, dtype=np.bool_)
    source = np.full(cfg.num_slices, -1, dtype=np.int64)
    for i, slice_img in enumerate(norm):
        volume[i] = resize_slice(slice_img, cfg.height, cfg.width, pad)
        mask[i] = True
        source[i] = idx[i]
    return PlaneTensor(
        plane=str(series.plane),
        series_id=series.series_id,
        volume=volume,
        mask=mask,
        source_slice_index=source,
        present=True,
    )


def empty_plane(plane: str, cfg: PreprocessingConfig) -> PlaneTensor:
    return PlaneTensor(
        plane=plane,
        series_id=None,
        volume=np.zeros((cfg.num_slices, cfg.height, cfg.width), dtype=np.float32),
        mask=np.zeros(cfg.num_slices, dtype=np.bool_),
        source_slice_index=np.full(cfg.num_slices, -1, dtype=np.int64),
        present=False,
    )


def preprocess_study(
    study_id: str, series_by_plane: dict[str, SeriesVolume], cfg: PreprocessingConfig
) -> PreprocessedStudy:
    """Build the model input for one study.

    ``series_by_plane`` holds at most one selected series per plane (series selection is
    the adapter's job). Missing planes become zero volumes with ``present=False`` and an
    all-false mask; the model must not treat them as real images.
    """
    warnings: list[str] = []
    planes: dict[str, PlaneTensor] = {}
    for plane in cfg.planes:
        series = series_by_plane.get(plane)
        if series is None:
            planes[plane] = empty_plane(plane, cfg)
            warnings.append(f"{plane} series missing")
            continue
        if series.study_id != study_id:
            raise PreprocessingError(f"series {series.series_id} belongs to another study")
        planes[plane] = preprocess_series(series, cfg)
    return PreprocessedStudy(
        study_id=study_id, preprocessing_version=cfg.version, planes=planes, warnings=warnings
    )
