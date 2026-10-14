#!/usr/bin/env bash
# Run API (fixture mode, :8000) and web dev server (:5173) together. Ctrl-C stops both.
set -euo pipefail
cd "$(dirname "$0")/.."
scripts/dev-api.sh &
API_PID=$!
trap 'kill $API_PID 2>/dev/null || true' EXIT INT TERM
pnpm --dir web dev
