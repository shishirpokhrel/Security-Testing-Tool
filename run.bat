@echo off
SETLOCAL

cd /d "%~dp0"

IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) ELSE (
    call venv\Scripts\activate.bat
)

python securityscanner.py %*

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Execution failed with error code %ERRORLEVEL%
    pause
)

ENDLOCAL
