@echo off
SETLOCAL

cd /d "%~dp0"

REM Check for venv and activate
IF EXIST "venv" (
    call venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Please run 'run.bat' first to set it up.
    exit /b 1
)

echo ===================================================
echo Starting Security Scanner Web UI
echo ===================================================

REM Start Backend in a new window
echo Starting Backend Server...
start "Security Scanner Backend" cmd /k "python api.py"

REM Start Frontend
echo Starting Frontend...
cd frontend

IF NOT EXIST "node_modules" (
    echo Node modules not found. Installing dependencies...
    call npm install
)

echo Starting Vite Dev Server...
call npm run dev

ENDLOCAL
