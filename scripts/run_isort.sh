#!/usr/bin/env bash
# ---------------------------------------------------------
# run_isort.sh – wrapper for isort used by pre‑commit
# ---------------------------------------------------------
# Exit on any error, treat unset variables as errors,
# and propagate failures through pipelines.
set -euo pipefail

# If you manage your virtual environment with Poetry, uncomment:
#   poetry run isort "$@"
#
# Otherwise, just call isort directly (assumes it’s on $PATH).
uv run isort .