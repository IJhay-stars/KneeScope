import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Allow running with a plain interpreter (no editable install) as well as via uv.
for sub in ("contracts", "ml", "api", "src"):
    path = str(ROOT / sub)
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault("KNEESCOPE_MODE", "fixture")
os.environ.setdefault("KNEESCOPE_FINDING_PROFILE", "interaction_prototype")
