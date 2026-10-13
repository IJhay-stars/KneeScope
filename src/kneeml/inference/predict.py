"""Model I/O (contract 05). STUB until a real checkpoint exists."""

import zlib

from kneeml.constants import FINDINGS


def predict_exam(exam_id: str) -> dict[str, float]:
    """Return placeholder probabilities (deterministic per exam). NOT real model output."""
    return {name: (zlib.crc32(f"{exam_id}:{name}".encode()) % 1000) / 1000 for name in FINDINGS}
