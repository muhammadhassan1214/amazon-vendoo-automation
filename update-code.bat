@echo off
setlocal
TITLE Amazon-Vendoo Code Updater

echo =====================================================
echo Checking for Git...
echo =====================================================

REM 1. Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [CRITICAL ERROR] Git is not found!
    echo Please install Git to use the updater.
    pause
    exit /b
)

REM 2. Check if this is a valid Git repository
if not exist ".git" (
    echo [CRITICAL ERROR] This folder is not a Git repository.
    echo Please place this file in the root folder of your project.
    pause
    exit /b
)

echo.
echo =====================================================
echo Securing local changes...
echo =====================================================

REM 3. Stash local changes
REM This moves any changes you made to a temporary storage area
REM so they don't conflict with the new update.
git stash
if %errorlevel% neq 0 (
    echo [WARNING] Could not stash changes. Proceeding anyway...
) else (
    echo [INFO] Local changes stashed successfully.
)

echo.
echo =====================================================
echo Downloading latest updates...
echo =====================================================

REM 4. Pull the latest code
git pull
if %errorlevel% neq 0 (
    echo [ERROR] Update failed! Check your internet connection or Git permissions.
    pause
    exit /b
)

echo.
echo =====================================================
echo [SUCCESS] The bot is now up to date!
echo =====================================================

REM Optional: If you want to re-apply your local changes after updating,
REM remove the "REM" from the line below:
REM git stash pop

pause