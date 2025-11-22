@echo off
setlocal
TITLE Amazon-Vendoo Automation Launcher

REM 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo =====================================================
    echo CRITICAL ERROR: Python is not found!
    echo Please install Python from python.org and check "Add to PATH".
    echo =====================================================
    pause
    exit /b
)

REM 2. Check/Create Virtual Environment
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating 'venv'...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
    echo [INFO] 'venv' created successfully.
)

REM 3. Activate Virtual Environment
call venv\Scripts\activate

REM 4. Install/Update Requirements
echo [INFO] Checking for required libraries...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements. Check internet connection.
    pause
    exit /b
)
echo [SUCCESS] Libraries are ready.

echo.
echo =====================================================
echo Checking File Requirements...
echo =====================================================
echo.

REM 5. Verify 'data' folder exists
if not exist "%CD%\data" (
    echo [CRITICAL ERROR] The 'data' folder is missing!
    echo Expected location: "%CD%\data"
    echo.
    echo Please create the folder and try again.
    echo =====================================================
    pause
    exit /b
)

REM 6. Verify .csv files exist
if exist "%CD%\data\*.csv" (
    echo [INFO] CSV file found. Proceeding...
) else (
    echo [CRITICAL ERROR] No .csv files found in the 'data' folder!
    echo.
    echo Please add your 'amazon-asins.csv' file to:
    echo "%CD%\data"
    echo =====================================================
    pause
    exit /b
)

REM 7. Run the Main Script
echo.
echo =====================================================
echo Starting Amazon-Vendoo Automation...
echo =====================================================
echo.
echo [TIP] To stop the bot, press Ctrl+C.
echo [TIP] If asked "Terminate batch job (Y/N)?", type N to ensure Chrome closes.
echo.

REM Fix for import errors: Add src to PYTHONPATH
set "PYTHONPATH=%CD%\src;%PYTHONPATH%"

REM Run the script
python src\main.py

REM =====================================================
REM 8. CLEANUP SECTION (Runs after script stops/crashes)
REM =====================================================
echo.
echo =====================================================
echo [CLEANUP] Stopping Chrome Driver and Browser...
echo =====================================================

REM This kills the ChromeDriver process (which usually closes the browser window)
taskkill /F /IM chromedriver.exe /T >nul 2>&1

REM Optional: If you want to aggressively kill ALL Chrome instances (Use with caution!)
REM Remove "REM" from the line below only if standard cleanup isn't working.
REM taskkill /F /IM chrome.exe /T >nul 2>&1

echo Process finished.
pause