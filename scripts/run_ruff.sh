#!/usr/bin/env bash
# ---------------------------------------------------------
# run_ruff.sh – wrapper for ruff used by pre‑commit
# ---------------------------------------------------------
set -euo pipefail

# Run ruff in “check + fix” mode.
# If you use Poetry, you can do: poetry run ruff check "$@" --fix
uv run ruff check "$@" --fix