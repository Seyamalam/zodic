# GitHub Workflows

This directory contains GitHub Actions workflows for the Zodic project.

## Workflows

### `tests.yml` - Continuous Integration
- Runs on push to `main` and `develop` branches
- Runs on pull requests to `main`
- Tests across Python 3.9, 3.10, 3.11, 3.12
- Tests on Ubuntu, Windows, and macOS
- Includes code quality checks (black, isort, flake8, mypy, bandit)
- Generates coverage reports
- Runs performance benchmarks

### `release.yml` - Release Automation
- Triggered by version tags (v*)
- Runs tests before release
- Builds and publishes to PyPI
- Creates GitHub releases with changelog
- Sends notifications (if configured)

### `dependencies.yml` - Dependency Management
- Runs weekly on Mondays
- Updates dependencies using Poetry
- Creates pull requests for dependency updates
- Runs security audits with safety and bandit

## Configuration

### Required Secrets
- `PYPI_API_TOKEN` - PyPI API token for publishing packages
- `DISCORD_WEBHOOK_URL` - (Optional) Discord webhook for release notifications

### Poetry Integration
All workflows use Poetry for dependency management. The project uses:
- `poetry install --with test,dev` for full development setup
- `poetry install --with dev` for code quality tools only
- `poetry build` for package building
- `poetry publish` for PyPI publishing

### Coverage Requirements
- Minimum coverage: 85%
- Coverage reports uploaded to Codecov
- HTML coverage reports available as artifacts

### Performance Monitoring
- Benchmarks run on every test
- Results stored as artifacts
- Uses pytest-benchmark for performance testing

## Dependabot Configuration
Dependabot is configured to:
- Update Python dependencies weekly
- Update GitHub Actions weekly
- Create PRs with appropriate labels
- Assign to project maintainer

Note: While Dependabot uses "pip" ecosystem, it works with Poetry projects by reading the exported requirements.txt and poetry.lock files.