#!/usr/bin/env bash
# ---------------------------------------------------------
# run_black.sh – wrapper for Black that auto‑adds changes
# ---------------------------------------------------------
set -euo pipefail

# Run Black (it will rewrite files if needed)
uv run isort "$@"

# If any files were changed, `black` exits with code 0 but
# leaves the modifications on disk. We now add them to the index.
if git diff --quiet; then
  # No changes – nothing to add
  exit 0
else
  # Stage the modified files so the commit can continue
  git add -u
  exit 0
fi