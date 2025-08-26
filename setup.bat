@echo off
echo Installing Telegram Channel Export Bot...
echo.

REM Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found, proceeding with setup...
echo.

REM Install requirements
echo Installing Python dependencies...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Create directories
echo Creating necessary directories...
if not exist "exports" mkdir exports
if not exist "exports\media" mkdir "exports\media"

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Copy .env.example to .env and configure your bot settings
echo 2. Get your bot token from @BotFather on Telegram
echo 3. Get API credentials from https://my.telegram.org
echo 4. Run: py bot.py
echo.
pause