#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Running pytest..."
python3 -m pytest "$ROOT/tests/" -v --tb=short

echo ""
echo "All tests passed."
