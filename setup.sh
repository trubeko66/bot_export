#!/bin/bash

echo "🚀 Setting up Telegram Channel Export Bot..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

echo "✅ Python found, proceeding with setup..."
echo

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Python version: $python_version"

# Install requirements
echo "📦 Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "✅ Dependencies installed successfully!"
echo

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p exports
mkdir -p exports/media

echo
echo "✅ Setup completed successfully!"
echo

echo "📋 Next steps:"
echo "1. Copy .env.example to .env and configure your bot settings:"
echo "   cp .env.example .env"
echo "   nano .env  # Edit with your credentials"
echo
echo "2. Get your bot token from @BotFather on Telegram"
echo "3. Get API credentials from https://my.telegram.org"
echo "4. Run the bot:"
echo "   python3 bot.py"
echo

echo "🎉 Ready to go! Happy exporting!"