@echo off
echo ========================================
echo Zodic Poetry Publishing
echo ========================================
echo.

echo Choose publishing option:
echo 1. Publish to TestPyPI (recommended first)
echo 2. Publish to PyPI (production)
echo 3. Just show publish commands
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Publishing to TestPyPI...
    echo Make sure you have configured TestPyPI token:
    echo poetry config repositories.testpypi https://test.pypi.org/legacy/
    echo poetry config pypi-token.testpypi your-testpypi-token
    echo.
    pause
    poetry publish -r testpypi
    echo.
    echo ✅ Published to TestPyPI!
    echo Test installation with:
    echo pip install --index-url https://test.pypi.org/simple/ zodic
) else if "%choice%"=="2" (
    echo.
    echo Publishing to PyPI...
    echo Make sure you have configured PyPI token:
    echo poetry config pypi-token.pypi your-pypi-token
    echo.
    pause
    poetry publish
    echo.
    echo ✅ Published to PyPI!
    echo Test installation with:
    echo pip install zodic
) else if "%choice%"=="3" (
    echo.
    echo Publishing Commands:
    echo.
    echo For TestPyPI:
    echo   poetry config repositories.testpypi https://test.pypi.org/legacy/
    echo   poetry config pypi-token.testpypi your-testpypi-token
    echo   poetry publish -r testpypi
    echo.
    echo For PyPI:
    echo   poetry config pypi-token.pypi your-pypi-token
    echo   poetry publish
    echo.
) else (
    echo Invalid choice!
)

pause