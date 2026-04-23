@echo off
if "%~1"=="" (
    python -X utf8 "%~dp0src\nythsleep.py" -h
    exit /b 0
)
python -X utf8 "%~dp0src\nythsleep.py" %*
