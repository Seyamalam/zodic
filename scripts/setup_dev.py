#!/usr/bin/env python3
"""
Development environment setup script for Zodic.

This script sets up everything needed for development:
1. Installs Poetry if needed
2. Installs dependencies
3. Sets up pre-commit hooks
4. Runs initial tests
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, check=True):
    """Run a command and return the result."""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    print(f"✅ Success")
    return True


def check_poetry():
    """Check if Poetry is installed."""
    result = subprocess.run("poetry --version", shell=True, capture_output=True)
    return result.returncode == 0


def install_poetry():
    """Install Poetry."""
    print("📦 Installing Poetry...")
    if os.name == 'nt':  # Windows
        cmd = 'powershell -Command "& {(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -}"'
    else:  # Unix-like
        cmd = 'curl -sSL https://install.python-poetry.org | python3 -'
    
    return run_command(cmd)


def setup_poetry():
    """Configure Poetry settings."""
    print("⚙️ Configuring Poetry...")
    run_command("poetry config virtualenvs.in-project true")
    run_command("poetry config virtualenvs.create true")


def install_dependencies():
    """Install project dependencies."""
    print("📚 Installing dependencies...")
    return run_command("poetry install --with dev,test")


def setup_pre_commit():
    """Set up pre-commit hooks."""
    print("🪝 Setting up pre-commit hooks...")
    
    # Create pre-commit config if it doesn't exist
    precommit_config = Path(".pre-commit-config.yaml")
    if not precommit_config.exists():
        config_content = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
"""
        precommit_config.write_text(config_content.strip())
        print("✅ Created .pre-commit-config.yaml")
    
    # Install pre-commit hooks
    return run_command("poetry run pre-commit install")


def run_initial_tests():
    """Run initial tests to verify setup."""
    print("🧪 Running initial tests...")
    return run_command("poetry run pytest tests/ -v")


def run_quality_checks():
    """Run code quality checks."""
    print("🔍 Running quality checks...")
    success = True
    
    success &= run_command("poetry run black --check zodic tests", check=False)
    success &= run_command("poetry run isort --check-only zodic tests", check=False)
    success &= run_command("poetry run flake8 zodic tests", check=False)
    success &= run_command("poetry run mypy zodic", check=False)
    
    return success


def create_vscode_settings():
    """Create VS Code settings for the project."""
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    settings = {
        "python.defaultInterpreterPath": "./.venv/bin/python",
        "python.formatting.provider": "black",
        "python.linting.enabled": True,
        "python.linting.flake8Enabled": True,
        "python.linting.mypyEnabled": True,
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": ["tests/"],
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.organizeImports": True
        }
    }
    
    import json
    settings_file = vscode_dir / "settings.json"
    settings_file.write_text(json.dumps(settings, indent=2))
    print("✅ Created VS Code settings")


def main():
    """Main setup function."""
    print("🚀 Setting up Zodic development environment...")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    
    # Check/install Poetry
    if not check_poetry():
        print("📦 Poetry not found, installing...")
        if not install_poetry():
            print("❌ Failed to install Poetry")
            sys.exit(1)
    else:
        print("✅ Poetry is already installed")
    
    # Setup Poetry
    setup_poetry()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup pre-commit
    if not setup_pre_commit():
        print("❌ Failed to setup pre-commit hooks")
        sys.exit(1)
    
    # Create VS Code settings
    create_vscode_settings()
    
    # Run initial tests
    if not run_initial_tests():
        print("❌ Initial tests failed")
        sys.exit(1)
    
    # Run quality checks
    quality_ok = run_quality_checks()
    if not quality_ok:
        print("⚠️ Some quality checks failed, but setup is complete")
        print("Run 'poetry run black zodic tests' and 'poetry run isort zodic tests' to fix formatting")
    
    print("\n" + "=" * 50)
    print("🎉 Development environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment: poetry shell")
    print("2. Run tests: poetry run pytest")
    print("3. Start coding!")
    print("\n🛠️ Available commands:")
    print("- poetry run pytest                    # Run tests")
    print("- poetry run pytest --cov=zodic       # Run tests with coverage")
    print("- poetry run black zodic tests        # Format code")
    print("- poetry run isort zodic tests        # Sort imports")
    print("- poetry run mypy zodic               # Type checking")
    print("- poetry run flake8 zodic tests      # Linting")
    print("- poetry build                        # Build package")
    print("- poetry publish --dry-run            # Test publishing")


if __name__ == "__main__":
    main()