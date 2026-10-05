#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if ! command -v uv >/dev/null 2>&1; then
  echo "Install uv first (see README.md), reopen your terminal, and try again."
  exit 1
fi
for task_arg in "$@"; do
  if [ "$task_arg" = "d2-2" ]; then
    exec uv run --locked --group rag python start.py "$@"
  fi
  if [ "$task_arg" = "d2-1" ]; then
    exec uv run --locked --group prompting python start.py "$@"
  fi
done
exec uv run --locked python start.py "$@"
