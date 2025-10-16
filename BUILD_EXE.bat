@echo off
REM Build Workspace Organizer Executable

echo.
echo ============================================
echo  Workspace Organizer - Build Executable
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

REM Install dependencies if needed
echo Checking dependencies...
python -m pip install -r requirements.txt >nul 2>&1

REM Run the build
echo Building executable...
echo This may take a few minutes...
echo.

python build_exe.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo Build completed successfully!
echo ============================================
echo.
echo Your executable is at:
echo   dist\WorkspaceOrganizer.exe
echo.
echo You can now:
echo  1. Copy it to your Desktop
echo  2. Create a shortcut
echo  3. Share it with others (it's portable!)
echo.

pause
