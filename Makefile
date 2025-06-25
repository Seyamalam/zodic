# Zodic Development Makefile
# 
# This Makefile provides convenient commands for development tasks.
# Run 'make help' to see all available commands.

.PHONY: help install test lint format type-check security build clean dev-setup ci release

# Default target
help: ## Show this help message
	@echo "Zodic Development Commands"
	@echo "========================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development setup
dev-setup: ## Set up development environment
	@python scripts/setup_dev.py

install: ## Install dependencies
	@poetry install --with dev,test

# Testing
test: ## Run tests
	@poetry run pytest tests/ -v

test-cov: ## Run tests with coverage
	@poetry run pytest tests/ -v --cov=zodic --cov-report=term-missing --cov-report=html

test-watch: ## Run tests in watch mode
	@poetry run pytest-watch tests/

benchmark: ## Run performance benchmarks
	@poetry run python -m pytest benchmarks/ -v --benchmark-only

# Code quality
lint: ## Run linting checks
	@poetry run flake8 zodic tests

format: ## Format code
	@poetry run black zodic tests
	@poetry run isort zodic tests

format-check: ## Check code formatting
	@poetry run black --check zodic tests
	@poetry run isort --check-only zodic tests

type-check: ## Run type checking
	@poetry run mypy zodic

security: ## Run security checks
	@poetry run bandit -r zodic
	@poetry run safety check

# Quality gates
quality: format-check lint type-check ## Run all quality checks

ci: ## Run full CI pipeline locally
	@python scripts/ci_local.py

# Building and publishing
build: ## Build package
	@poetry build

build-check: ## Build and validate package
	@poetry build
	@poetry run twine check dist/*

publish-test: ## Publish to TestPyPI
	@poetry publish -r testpypi

publish: ## Publish to PyPI
	@poetry publish

# Release management
release: ## Create a new release (usage: make release VERSION=0.2.0)
	@python scripts/release.py $(VERSION)

# Maintenance
clean: ## Clean build artifacts
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

clean-all: clean ## Clean everything including virtual environment
	@poetry env remove python

# Documentation
docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

# Git hooks
pre-commit: ## Run pre-commit hooks
	@poetry run pre-commit run --all-files

install-hooks: ## Install git hooks
	@poetry run pre-commit install

# Development utilities
shell: ## Open poetry shell
	@poetry shell

deps-update: ## Update dependencies
	@poetry update

deps-export: ## Export dependencies to requirements.txt
	@poetry export -f requirements.txt --output requirements.txt --with dev

# Project information
info: ## Show project information
	@echo "Project: Zodic"
	@echo "Version: $$(poetry version -s)"
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$(poetry --version)"
	@echo "Virtual env: $$(poetry env info --path)"

# Quick development workflow
dev: install format test ## Quick development workflow: install, format, test

# Full workflow before pushing
ready: ci build-check ## Full workflow before pushing to GitHub