"""Inference boundary between the API and a trained model.

Rule: nothing in this module (or anything it imports) may read dataset labels.
``tests/test_label_isolation.py`` enforces this.
"""

from __future__ import annotations

from typing import Protocol

from kneescope_ml.config import ModelConfig
from kneescope_ml.types import ModelOutput, PreprocessedStudy


class ModelNotAvailableError(RuntimeError):
    """No checkpoint is configured or it failed verification."""


class Predictor(Protocol):
    model_id: str
    model_version: str
    checkpoint_sha256: str
    supported_findings: tuple[str, ...]

    def predict(self, study: PreprocessedStudy) -> ModelOutput: ...


def load_predictor(cfg: ModelConfig) -> Predictor:
    """Load and verify the configured checkpoint.

    Placeholder: the baseline model, checkpoint format and hash verification are
    implemented by KS-MODEL-03 and KS-MODEL-05.
    """
    if not cfg.has_checkpoint:
        raise ModelNotAvailableError("no checkpoint configured in config/model.toml")
    raise ModelNotAvailableError("checkpoint loading is not implemented yet (KS-MODEL-05)")
