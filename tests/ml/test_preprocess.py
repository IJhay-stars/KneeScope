import numpy as np
import pytest

from kneescope_ml.adapters.fixture import FixtureAdapter
from kneescope_ml.config import load_preprocessing_config
from kneescope_ml.preprocess import PreprocessingError, preprocess_study, sample_slice_indices
from kneescope_ml.types import SeriesVolume

CFG = load_preprocessing_config()


def test_sampling_is_ordered_without_repeats():
    idx = sample_slice_indices(100, 32)
    assert len(idx) == 32 and np.all(np.diff(idx) > 0)
    assert list(sample_slice_indices(10, 32)) == list(range(10))


def test_contract_shapes_masks_and_missing_plane():
    adapter = FixtureAdapter()
    refs = adapter.select_series("fx-study-004")  # coronal + axial only
    series = {p: adapter.load_series("fx-study-004", r.series_id) for p, r in refs.items()}
    out = preprocess_study("fx-study-004", series, CFG)
    assert set(out.planes) == {"sagittal", "coronal", "axial"}
    for plane in out.planes.values():
        assert plane.volume.dtype == np.float32
        assert plane.volume.shape == (CFG.num_slices, CFG.height, CFG.width)
        assert plane.mask.shape == (CFG.num_slices,)
    sag = out.planes["sagittal"]
    assert not sag.present and not sag.mask.any() and (sag.source_slice_index == -1).all()
    cor = out.planes["coronal"]
    assert cor.mask.sum() == 24 and (cor.source_slice_index[cor.mask] == np.arange(24)).all()
    assert "sagittal series missing" in out.warnings


def test_constant_and_invalid_series():
    flat = SeriesVolume("s", "x", "sagittal", np.ones((4, 8, 8), np.float32), "synthetic")
    out = preprocess_study("s", {"sagittal": flat}, CFG)
    assert np.allclose(out.planes["sagittal"].volume, 0)
    bad = SeriesVolume("s", "x", "sagittal", np.full((4, 8, 8), np.nan, np.float32), "synthetic")
    with pytest.raises(PreprocessingError):
        preprocess_study("s", {"sagittal": bad}, CFG)


def test_series_from_another_study_is_rejected():
    other = SeriesVolume("other", "x", "sagittal", np.ones((4, 8, 8), np.float32), "synthetic")
    with pytest.raises(PreprocessingError):
        preprocess_study("s", {"sagittal": other}, CFG)
