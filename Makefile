.PHONY: install-hooks
install-hooks:
	@echo "🔧 Installing pre‑commit and pre‑push hooks from .githooks/ ..."
	pre-commit install -c .pre-commit-config.yaml
	pre-commit install -c .pre-commit-config.yaml --hook-type pre-push
	@echo "✅ Hooks installed!"

.PHONY: secrets-baseline
secrets-baseline:
	@echo "🔍 Generating detect‑secrets baseline..."
	detect-secrets scan > .secrets.baseline
	@git add .secrets.baseline
	@git commit -m "Update detect‑secrets baseline"
	@echo "✅ Baseline updated and committed."