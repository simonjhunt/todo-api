#!/usr/bin/env bash
# ---------------------------------------------------------
# run_black.sh – wrapper for Black used by pre‑commit
# ---------------------------------------------------------
# Exit immediately on any error, treat unset variables as errors,
# and propagate failures through pipes.
set -euo pipefail

# If you use Poetry, uncomment the next line so the script runs
# inside the project's virtual environment:
#   poetry run black "$@"
#
# If you rely on a globally installed Black (or a venv already active),
# the plain command works:
uv run black .