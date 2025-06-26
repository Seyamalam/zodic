poetry run black --check --diff zodic tests
poetry run isort --check-only --diff zodic tests
poetry run mypy zodic
poetry run bandit -r zodic
poetry run bandit -r zodic
poetry run safety check