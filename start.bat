@echo off
title Telegram Channel Export Bot
echo.
echo ========================================
echo   Telegram Channel Export Bot v1.0.0
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found!
    echo.
    echo Please create .env file from .env.example:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env with your bot credentials
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Check if exports directory exists
if not exist "exports" (
    echo 📁 Creating exports directory...
    mkdir exports
)

if not exist "exports\media" (
    echo 📁 Creating media directory...
    mkdir "exports\media"
)

echo 🚀 Starting Telegram Channel Export Bot...
echo.
echo 📋 Press Ctrl+C to stop the bot
echo.

REM Start the bot
py bot.py

if errorlevel 1 (
    echo.
    echo ❌ Bot stopped with an error!
    echo.
    echo Common issues:
    echo   - Check your .env configuration
    echo   - Ensure all dependencies are installed
    echo   - Verify your bot token and API credentials
    echo.
    pause
) else (
    echo.
    echo ✅ Bot stopped successfully!
    pause
)