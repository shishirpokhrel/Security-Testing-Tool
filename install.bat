@echo off
REM Installation script for Windows

echo ==========================================
echo Security Scanner - Installation Script
echo ==========================================
echo.

REM Check Python version
echo Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    echo [OK] Python found
    python --version
) else (
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=py
        echo [OK] Python launcher found
        py --version
    ) else (
        echo [ERROR] Python not found!
        echo Please install Python from python.org or Microsoft Store
        pause
        exit /b 1
    )
)

echo.
echo ==========================================
echo Installing Python dependencies...
echo ==========================================
echo.

REM Upgrade pip
echo Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing packages from requirements.txt...
%PYTHON_CMD% -m pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Python dependencies installed successfully!
) else (
    echo.
    echo [ERROR] Failed to install dependencies
    echo Try running manually:
    echo   %PYTHON_CMD% -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Checking external dependencies...
echo ==========================================
echo.

REM Check for Nmap
where nmap >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Nmap found
    nmap --version
) else (
    echo [WARNING] Nmap not found
    echo Download from: https://nmap.org/download.html
)

REM Check for Subfinder
where subfinder >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Subfinder found
    subfinder -version
) else (
    echo [INFO] Subfinder not found (optional)
    echo Download from: https://github.com/projectdiscovery/subfinder/releases
)

echo.
echo ==========================================
echo Running import test...
echo ==========================================
echo.

%PYTHON_CMD% test_imports.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo [OK] Installation successful!
    echo ==========================================
    echo.
    echo To run the scanner:
    echo   %PYTHON_CMD% securityscanner.py
    echo.
    echo For help:
    echo   %PYTHON_CMD% securityscanner.py --help
    echo.
) else (
    echo.
    echo ==========================================
    echo [ERROR] Installation incomplete
    echo ==========================================
    echo.
    echo Please check the errors above and fix them.
    pause
    exit /b 1
)

pause
