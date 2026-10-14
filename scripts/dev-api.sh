#!/usr/bin/env bash
# Run the API in fixture mode on http://localhost:8000 (docs at /docs).
set -euo pipefail
cd "$(dirname "$0")/.."
export KNEESCOPE_MODE="${KNEESCOPE_MODE:-fixture}"
exec uv run uvicorn kneescope_api.main:app --host 127.0.0.1 --port "${PORT:-8000}" --reload \
  --reload-dir api --reload-dir ml --reload-dir contracts
