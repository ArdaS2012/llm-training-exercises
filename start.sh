#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if ! command -v uv >/dev/null 2>&1; then
  echo "Install uv first (see README.md), reopen your terminal, and try again."
  exit 1
fi
exec uv run --locked python start.py "$@"
