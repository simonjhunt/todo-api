# .githooks/scripts/run_ruff.sh
#!/usr/bin/env bash
set -euo pipefail
uv run ruff check "$@" --fix