"""Shared preprocessing (contract 04). Training, evaluation and the API must all call this."""

import numpy as np


def preprocess_exam(volumes: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """STUB: per-plane intensity normalisation. M1 replaces with the real pipeline."""
    out: dict[str, np.ndarray] = {}
    for plane, volume in volumes.items():
        v = volume.astype("float32")
        out[plane] = (v - v.mean()) / (v.std() + 1e-6)
    return out
