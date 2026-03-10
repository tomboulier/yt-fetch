.DEFAULT_GOAL := help

.PHONY: install
install: ## Install the virtual environment
	@echo "🚀 Creating virtual environment using uv"
	@uv venv
	@uv sync --all-groups

.PHONY: check
check: ## Run code quality tools
	@echo "🚀 Linting code: Running ruff"
	@uv run ruff check src tests
	@echo "🚀 Checking formatting: Running ruff format"
	@uv run ruff format --check src tests

.PHONY: fmt
fmt: ## Auto-format code with ruff
	@uv run ruff format src tests
	@uv run ruff check --fix src tests

.PHONY: test
test: ## Run tests with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run pytest --cov --cov-report=term-missing

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@uv run python -c "import shutil, os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: publish
publish: ## Publish to PyPI
	@echo "🚀 Publishing to PyPI"
	@uvx twine upload dist/*

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"
