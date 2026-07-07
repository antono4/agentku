@echo off
chcp 65001 >nul
title Scheduled Concurrent Agent

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Load .env if exists
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (`findstr /v "^#" .env`) do (
        set "%%a=%%b"
    )
)

REM Run agent in interactive mode
python scheduled_concurrent_agent.py --interactive

pause
