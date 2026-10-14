"""Shared KneeScope contracts. See contracts/README.md."""

from kneescope_contracts.findings import load_profile
from kneescope_contracts.models import SCHEMA_VERSION

__all__ = ["SCHEMA_VERSION", "load_profile"]
