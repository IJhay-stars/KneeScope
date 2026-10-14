"""Display rendering of a single slice to 8-bit PNG (shared by API and tooling).

This is a display rendering: per-series percentile scaling to 0-255. It is not MRI
window/level and must not be described as such in the UI (DESIGN.md section 14).
"""

from __future__ import annotations

import io

import numpy as np
from PIL import Image, ImageDraw

from kneescope_ml.config import PreprocessingConfig
from kneescope_ml.types import SeriesVolume


def rendered_size(rows: int, cols: int, max_size: int) -> tuple[int, int]:
    """(width, height) of the PNG the slice endpoint returns for a series."""
    scale = min(1.0, max_size / max(rows, cols))
    return max(1, round(cols * scale)), max(1, round(rows * scale))


def render_slice_png(
    series: SeriesVolume, index: int, cfg: PreprocessingConfig, watermark: str | None = None
) -> bytes:
    n, rows, cols = series.pixels.shape
    if not 0 <= index < n:
        raise IndexError(f"slice_index {index} out of range 0..{n - 1}")
    lo, hi = np.percentile(series.pixels, [cfg.render_p_low, cfg.render_p_high])
    span = max(float(hi - lo), 1e-6)
    img8 = (np.clip((series.pixels[index] - lo) / span, 0, 1) * 255).astype(np.uint8)
    image = Image.fromarray(img8, mode="L")
    size = rendered_size(rows, cols, cfg.render_max_size)
    if size != (cols, rows):
        image = image.resize(size, Image.Resampling.BILINEAR)
    if watermark:
        ImageDraw.Draw(image).text((6, size[1] - 14), watermark, fill=200)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
