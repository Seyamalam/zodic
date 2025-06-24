@echo off
echo ========================================
echo Zodic Poetry Clean & Reset
echo ========================================
echo.

echo [1/5] Removing virtual environment...
poetry env remove python

echo [2/5] Clearing Poetry cache...
poetry cache clear pypi --all

echo [3/5] Removing build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist htmlcov rmdir /s /q htmlcov

echo [4/5] Removing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc >nul 2>&1

echo [5/5] Removing coverage files...
del .coverage >nul 2>&1
del coverage.xml >nul 2>&1

echo.
echo ✅ Clean complete! 
echo Run poetry_workflow.bat to start fresh.
pause