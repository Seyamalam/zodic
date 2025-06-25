#!/usr/bin/env python3
"""
Local CI simulation script.

This script runs the same checks that run in CI/CD locally,
allowing developers to catch issues before pushing.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd, description, allow_failure=False):
    """Run a command with timing and status reporting."""
    print(f"\n🔧 {description}...")
    print(f"Command: {cmd}")
    
    start_time = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    end_time = time.time()
    duration = end_time - start_time
    
    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS ({duration:.2f}s)")
        return True
    else:
        print(f"❌ {description} - FAILED ({duration:.2f}s)")
        if result.stdout:
            print("STDOUT:", result.stdout[-500:])  # Last 500 chars
        if result.stderr:
            print("STDERR:", result.stderr[-500:])  # Last 500 chars
        
        if not allow_failure:
            return False
        else:
            print("⚠️ Continuing despite failure...")
            return True


def check_environment():
    """Check if the environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check if we're in a Poetry project
    if not Path("pyproject.toml").exists():
        print("❌ Not in a Poetry project directory")
        return False
    
    # Check if Poetry is available
    result = subprocess.run("poetry --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("❌ Poetry not found")
        return False
    
    print("✅ Environment check passed")
    return True


def run_tests():
    """Run the test suite."""
    return run_command(
        "poetry run pytest tests/ -v --cov=zodic --cov-report=term-missing --cov-fail-under=85",
        "Running test suite"
    )


def run_formatting_check():
    """Check code formatting."""
    return run_command(
        "poetry run black --check --diff zodic tests",
        "Checking code formatting"
    )


def run_import_sorting_check():
    """Check import sorting."""
    return run_command(
        "poetry run isort --check-only --diff zodic tests",
        "Checking import sorting"
    )


def run_linting():
    """Run linting checks."""
    return run_command(
        "poetry run flake8 zodic tests",
        "Running linting checks"
    )


def run_type_checking():
    """Run type checking."""
    return run_command(
        "poetry run mypy zodic",
        "Running type checking",
        allow_failure=True  # Type checking warnings are non-blocking
    )


def run_security_checks():
    """Run security checks."""
    success = True
    success &= run_command(
        "poetry run bandit -r zodic",
        "Running security scan (bandit)",
        allow_failure=True
    )
    success &= run_command(
        "poetry run safety check",
        "Checking dependency security (safety)",
        allow_failure=True
    )
    return success


def run_build_test():
    """Test building the package."""
    return run_command(
        "poetry build",
        "Building package"
    ) and run_command(
        "poetry run twine check dist/*",
        "Validating package"
    )


def run_benchmarks():
    """Run performance benchmarks."""
    return run_command(
        "poetry run python -m pytest benchmarks/ -v --benchmark-only",
        "Running performance benchmarks",
        allow_failure=True
    )


def auto_fix_issues():
    """Automatically fix common issues."""
    print("\n🔧 Auto-fixing common issues...")
    
    # Fix formatting
    run_command(
        "poetry run black zodic tests",
        "Auto-fixing code formatting",
        allow_failure=True
    )
    
    # Fix import sorting
    run_command(
        "poetry run isort zodic tests",
        "Auto-fixing import sorting",
        allow_failure=True
    )
    
    print("✅ Auto-fixes applied")


def main():
    """Main CI simulation function."""
    print("🚀 Running Local CI Simulation")
    print("=" * 60)
    
    start_time = time.time()
    
    # Environment check
    if not check_environment():
        sys.exit(1)
    
    # Track results
    results = {}
    
    # Install dependencies
    results["deps"] = run_command(
        "poetry install --with dev,test",
        "Installing dependencies"
    )
    
    # Run all checks
    results["tests"] = run_tests()
    results["formatting"] = run_formatting_check()
    results["imports"] = run_import_sorting_check()
    results["linting"] = run_linting()
    results["typing"] = run_type_checking()
    results["security"] = run_security_checks()
    results["build"] = run_build_test()
    results["benchmarks"] = run_benchmarks()
    
    # Summary
    end_time = time.time()
    total_duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("📊 CI Simulation Results")
    print("=" * 60)
    
    passed = 0
    total = 0
    
    for check, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{check.ljust(15)}: {status}")
        if success:
            passed += 1
        total += 1
    
    print(f"\nTotal: {passed}/{total} checks passed")
    print(f"Duration: {total_duration:.2f} seconds")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready to push to GitHub.")
        return True
    else:
        print(f"\n❌ {total - passed} checks failed.")
        
        # Offer to auto-fix
        if not results["formatting"] or not results["imports"]:
            response = input("\n🔧 Auto-fix formatting and import issues? (y/n): ")
            if response.lower() == 'y':
                auto_fix_issues()
                print("\n🔄 Re-run the script to verify fixes.")
        
        print("\n💡 Tips:")
        if not results["formatting"]:
            print("- Run: poetry run black zodic tests")
        if not results["imports"]:
            print("- Run: poetry run isort zodic tests")
        if not results["linting"]:
            print("- Check flake8 output and fix linting issues")
        if not results["tests"]:
            print("- Fix failing tests before pushing")
        
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)