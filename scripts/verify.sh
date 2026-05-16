#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Checking Python syntax..."
python3 -m py_compile "$ROOT/calendar_bot.py"
echo "    calendar_bot.py OK"

echo "==> Checking .env.example has all required variables..."
REQUIRED_VARS=(GOOGLE_API_KEY CALENDAR_ID TELEGRAM_BOT_TOKEN TELEGRAM_GROUP_ID)
for var in "${REQUIRED_VARS[@]}"; do
  if ! grep -q "^${var}=" "$ROOT/.env.example"; then
    echo "    ERROR: ${var} missing from .env.example" >&2
    exit 1
  fi
done
echo "    .env.example OK"

echo "==> Checking requirements.txt is up to date with requirements.in..."
if command -v pip-compile &>/dev/null; then
  pip-compile --dry-run "$ROOT/requirements.in" --output-file "$ROOT/requirements.txt" &>/dev/null \
    && echo "    requirements.txt OK" \
    || echo "    WARNING: requirements.txt may be out of date (run pip-compile requirements.in)"
else
  echo "    SKIP: pip-compile not installed"
fi

echo ""
echo "verify.sh passed."
