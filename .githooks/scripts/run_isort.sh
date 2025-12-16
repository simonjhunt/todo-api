# .githooks/scripts/run_isort.sh
#!/usr/bin/env bash
set -euo pipefail
uv run isort "$@"