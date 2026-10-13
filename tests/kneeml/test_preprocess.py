import numpy as np

from kneeml.data.preprocess import preprocess_exam


def test_preprocess_keeps_shape_and_normalises() -> None:
    vol = np.random.default_rng(0).normal(100, 20, size=(8, 16, 16))
    out = preprocess_exam({"sagittal": vol})["sagittal"]
    assert out.shape == vol.shape
    assert abs(float(out.mean())) < 1e-3
