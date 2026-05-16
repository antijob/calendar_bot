#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="$ROOT/docs"

REQUIRED_DOCS=(setup.md configuration.md deployment.md)

echo "==> Checking docs/ directory exists..."
if [[ ! -d "$DOCS_DIR" ]]; then
  echo "    ERROR: docs/ directory not found" >&2
  exit 1
fi
echo "    docs/ found"

echo "==> Checking required doc files..."
MISSING=0
for doc in "${REQUIRED_DOCS[@]}"; do
  path="$DOCS_DIR/$doc"
  if [[ ! -f "$path" ]]; then
    echo "    ERROR: missing $doc" >&2
    MISSING=1
  elif [[ ! -s "$path" ]]; then
    echo "    ERROR: $doc is empty" >&2
    MISSING=1
  else
    echo "    $doc OK"
  fi
done

if [[ "$MISSING" -ne 0 ]]; then
  exit 1
fi

echo "==> Checking AGENTS.md links to all doc files..."
AGENTS_MD="$ROOT/AGENTS.md"
for doc in "${REQUIRED_DOCS[@]}"; do
  if ! grep -q "docs/${doc}" "$AGENTS_MD"; then
    echo "    WARNING: AGENTS.md does not link to docs/${doc}"
  fi
done

echo ""
echo "check-docs.sh passed."
