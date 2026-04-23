@echo off
if "%~1"=="" (
    echo Error: 'nsleep' is a quick command exclusively for argument parsing.
    echo Please provide arguments (e.g., nsleep -s -t 20m) or use 'nythsleep' for the interactive menu.
    exit /b 1
)
python -X utf8 "%~dp0src\nythsleep.py" %*
