@echo off
echo ========================================
echo Zodic Quick Poetry Workflow
echo ========================================
echo.

REM Quick workflow for when you just want to test changes
echo [1/4] Installing/updating dependencies...
poetry install --quiet

echo [2/4] Running tests...
poetry run pytest tests/ -q

echo [3/4] Building package...
poetry build --quiet

echo [4/4] Testing publish (dry-run)...
poetry publish --dry-run

echo.
echo ✅ Quick workflow complete!
echo Ready to publish with: poetry publish
pause