#!/usr/bin/env python3
"""
Test script to simulate GitHub Actions workflow locally.
This tests the same commands that will run in CI/CD.
"""

import subprocess
import sys
import os

def run_command(cmd, description, allow_failure=False):
    """Run a command and return success status."""
    print(f"\n🔧 {description}...")
    print(f"Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                # Only show last few lines to avoid spam
                lines = result.stdout.strip().split('\n')
                if len(lines) > 10:
                    print("Output (last 10 lines):")
                    for line in lines[-10:]:
                        print(f"  {line}")
                else:
                    print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return allow_failure
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return allow_failure

def test_workflow():
    """Test the GitHub Actions workflow locally."""
    print("🚀 Testing GitHub Actions Workflow Locally")
    print("=" * 60)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Step 1: Install Poetry (if not already installed)
    if not run_command("poetry --version", "Checking Poetry installation", allow_failure=True):
        print("Installing Poetry...")
        if not run_command("pip install poetry", "Installing Poetry"):
            return False
    
    # Step 2: Install dependencies (test group)
    if not run_command("poetry install --with test", "Installing test dependencies"):
        return False
    
    # Step 3: Run tests with coverage
    if not run_command("poetry run pytest tests/ -v --cov=zodic --cov-report=xml", "Running tests with coverage"):
        return False
    
    # Step 4: Install dev dependencies
    if not run_command("poetry install --with dev", "Installing dev dependencies"):
        return False
    
    # Step 5: Check code formatting
    if not run_command("poetry run black --check zodic tests", "Checking code formatting", allow_failure=True):
        print("⚠️  Code formatting issues found. This would fail in CI.")
        print("Run: poetry run black zodic tests")
    
    # Step 6: Check import sorting
    if not run_command("poetry run isort --check-only zodic tests", "Checking import sorting", allow_failure=True):
        print("⚠️  Import sorting issues found. This would fail in CI.")
        print("Run: poetry run isort zodic tests")
    
    # Step 7: Run type checking
    if not run_command("poetry run mypy zodic", "Running type checking", allow_failure=True):
        print("⚠️  Type checking issues found. This would fail in CI.")
    
    # Step 8: Run linting
    if not run_command("poetry run flake8 zodic", "Running linting", allow_failure=True):
        print("⚠️  Linting issues found. This would fail in CI.")
    
    print("\n" + "=" * 60)
    print("🎯 GitHub Workflow Test Summary")
    print("=" * 60)
    
    # Check if coverage file was created
    if os.path.exists("coverage.xml"):
        print("✅ Coverage report generated")
    else:
        print("❌ Coverage report not found")
    
    print("\n📋 Next Steps:")
    print("1. Fix any formatting/linting issues shown above")
    print("2. Commit and push to GitHub to trigger actual CI/CD")
    print("3. Check GitHub Actions tab for results")
    
    return True

def fix_issues():
    """Auto-fix common issues."""
    print("\n🔧 Auto-fixing common issues...")
    
    # Fix formatting
    run_command("poetry run black zodic tests", "Auto-fixing code formatting")
    
    # Fix import sorting
    run_command("poetry run isort zodic tests", "Auto-fixing import sorting")
    
    print("✅ Auto-fixes applied. Re-run the test to check.")

def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        fix_issues()
        return
    
    success = test_workflow()
    
    if not success:
        print("\n❌ Workflow test failed!")
        print("Run with --fix to auto-fix formatting issues:")
        print("python test_github_workflow.py --fix")
        sys.exit(1)
    else:
        print("\n🎉 Workflow test completed!")
        print("Your code should pass GitHub Actions CI/CD.")

if __name__ == "__main__":
    main()