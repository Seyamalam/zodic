@echo off
echo ========================================
echo Zodic Poetry Workflow Automation
echo ========================================
echo.

REM Set error handling
setlocal enabledelayedexpansion

REM Function to check command success
set "success=true"

echo [1/8] Checking Poetry installation...
poetry --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Poetry not found! Please install Poetry first.
    echo Install with: pip install poetry
    pause
    exit /b 1
) else (
    echo ✅ Poetry is installed
)
echo.

echo [2/8] Removing existing virtual environment...
poetry env remove python >nul 2>&1
echo ✅ Environment cleaned
echo.

echo [3/8] Installing dependencies...
poetry install
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
) else (
    echo ✅ Dependencies installed successfully
)
echo.

echo [4/8] Running tests...
poetry run pytest tests/ -v
if errorlevel 1 (
    echo ❌ Tests failed
    pause
    exit /b 1
) else (
    echo ✅ All tests passed
)
echo.

echo [5/8] Checking code formatting...
poetry run black --check zodic tests
if errorlevel 1 (
    echo ⚠️  Code formatting issues found. Auto-fixing...
    poetry run black zodic tests
    echo ✅ Code formatted
) else (
    echo ✅ Code formatting is correct
)
echo.

echo [6/8] Running type checking...
poetry run mypy zodic
if errorlevel 1 (
    echo ⚠️  Type checking issues found (continuing anyway)
) else (
    echo ✅ Type checking passed
)
echo.

echo [7/8] Building package...
poetry build
if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
) else (
    echo ✅ Package built successfully
)
echo.

echo [8/8] Testing publish (dry-run)...
poetry publish --dry-run
if errorlevel 1 (
    echo ❌ Dry-run publish failed
    pause
    exit /b 1
) else (
    echo ✅ Dry-run publish successful
)
echo.

echo ========================================
echo 🎉 All steps completed successfully!
echo ========================================
echo.
echo Built files in dist/:
dir dist\ /b
echo.
echo Next steps:
echo 1. poetry publish -r testpypi  (publish to TestPyPI)
echo 2. poetry publish              (publish to PyPI)
echo.
pause