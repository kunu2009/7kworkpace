@echo off
REM Workspace Organizer - Install and Run Script

echo.
echo ============================================
echo  Workspace Organizer - Setup & Run
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Run the application
echo Starting Workspace Organizer...
python main.py

pause
