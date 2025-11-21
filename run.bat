@echo off
TITLE Amazon-Vendoo Automation Launcher

:: 1. Check if Python is installed on the user's computer
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo =====================================================
    echo CRITICAL ERROR: Python is not found!
    echo Please install Python from python.org and checks "Add to PATH".
    echo =====================================================
    pause
    exit
)

:: 2. Check if the Virtual Environment (venv) exists
:: If it doesn't exist (first run), we create it automatically.
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating 'venv'...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit
    )
    echo [INFO] 'venv' created successfully.
)

:: 3. Activate the Virtual Environment
call venv\Scripts\activate

:: 4. Install/Update Requirements
:: This runs every time to ensure the bot has the libraries it needs.
:: It is very fast if they are already installed.
echo [INFO] Checking for required libraries...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements. Check your internet connection.
    pause
    exit
)
echo [SUCCESS] Libraries are ready.

:: 5. Run the Main Script
echo.
echo =====================================================
echo Starting Amazon-Vendoo Automation...
echo =====================================================
echo.

:: Ensure src is on PYTHONPATH so absolute imports (utils, core) resolve
set PYTHONPATH=%CD%\src;%PYTHONPATH%

:: Point this to where your main file is located
python src\main.py

:: 6. Pause so the user can see the output or errors before the window closes
echo.
echo =====================================================
echo Process finished.
pause