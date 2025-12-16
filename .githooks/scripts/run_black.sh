# .githooks/scripts/run_black.sh
#!/usr/bin/env bash
# Fail fast if anything goes wrong
set -euo pipefail

# Use the same Python interpreter that runs pre‑commit
# (if you use Poetry, you can activate the venv here)
uv run black .