.PHONY: install-hooks
install-hooks:
	@echo "🔧 Installing pre‑commit and pre‑push hooks from .githooks/ ..."
	pre-commit install -c .githooks/.pre-commit-config.yaml
	pre-commit install -c .githooks/.pre-commit-config.yaml --hook-type pre-push
	@echo "✅ Hooks installed!"