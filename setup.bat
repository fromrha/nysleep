@echo off
setlocal

echo ================================================
echo           Nythsleep Global Setup
echo ================================================
echo.

where pipx >nul 2>&1
if errorlevel 1 (
    echo [!] pipx was not found.
    echo Install Python 3.9+ first, then run:
    echo     py -m pip install --user pipx
    echo     py -m pipx ensurepath
    exit /b 1
)

pipx install "%~dp0" --force
if errorlevel 1 exit /b 1
pipx ensurepath

echo.
echo [+] Nythsleep installed. Open a new terminal, then run:
echo     nythsleep --help
pause
