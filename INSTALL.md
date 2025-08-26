# Installation Guide - Telegram Channel Export Bot

This guide provides detailed installation instructions for different operating systems and setups.

## 📋 Prerequisites

### Required
- **Python 3.8 or higher** - [Download from python.org](https://python.org)
- **Telegram Bot Token** - Get from [@BotFather](https://t.me/BotFather)
- **Telegram API Credentials** - Get from [my.telegram.org](https://my.telegram.org)

### Optional
- **Git** - For cloning the repository
- **Code Editor** - For configuration editing

## 🖥️ Platform-Specific Installation

### Windows

#### Option 1: Quick Setup (Recommended)
1. **Download or clone the project**
2. **Run the setup script**:
   ```cmd
   setup.bat
   ```
3. **Configure credentials** (see Configuration section below)
4. **Start the bot**:
   ```cmd
   start.bat
   ```

#### Option 2: Manual Setup
1. **Install Python dependencies**:
   ```cmd
   py -m pip install -r requirements.txt
   ```
2. **Create directories**:
   ```cmd
   mkdir exports
   mkdir exports\media
   ```
3. **Configure and run** (see sections below)

### Linux/macOS

#### Option 1: Quick Setup (Recommended)
1. **Make setup script executable**:
   ```bash
   chmod +x setup.sh
   ```
2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```
3. **Configure credentials** (see Configuration section below)
4. **Start the bot**:
   ```bash
   python3 bot.py
   ```

#### Option 2: Manual Setup
1. **Install Python dependencies**:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. **Create directories**:
   ```bash
   mkdir -p exports/media
   ```
3. **Configure and run** (see sections below)

## 🔧 Configuration

### 1. Create Environment File
```bash
# Copy the example file
cp .env.example .env

# Edit with your preferred editor
nano .env        # Linux/macOS
notepad .env     # Windows
```

### 2. Configure Required Settings
Edit `.env` file with your credentials:

```env
# Required: Bot token from @BotFather
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789

# Required: API credentials from my.telegram.org
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890

# Optional: Your Telegram user ID
ADMIN_USER_ID=123456789

# Optional: Default settings
DEFAULT_EXPORT_FORMAT=json
INCLUDE_MEDIA_BY_DEFAULT=false
MAX_MESSAGES_PER_EXPORT=10000
```

### 3. Get Telegram Credentials

#### Bot Token
1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name for your bot
   - Choose a username (must end with 'bot')
4. Copy the provided token

#### API Credentials
1. Visit [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application:
   - App title: "Channel Export Bot"
   - Short name: "export_bot"
   - Platform: Other
5. Copy the `api_id` and `api_hash`

## 🚀 Running the Bot

### Windows
```cmd
# Using the start script
start.bat

# Or directly
py bot.py
```

### Linux/macOS
```bash
# Direct execution
python3 bot.py

# Or with specific Python version
python3.9 bot.py
```

## 🧪 Testing Installation

### 1. Test Dependencies
```bash
# Test all export formats
python3 test_export_formats.py

# Test markdown generation
python3 test_simple.py
```

### 2. Test Bot Connection
1. Start the bot
2. Send `/start` to your bot on Telegram
3. You should receive a welcome message

## 🔍 Troubleshooting

### Common Issues

#### "Module not found" Error
**Problem**: Missing Python dependencies
**Solution**:
```bash
pip install -r requirements.txt
```

#### "Invalid token" Error
**Problem**: Incorrect bot token
**Solution**:
1. Check your `.env` file
2. Ensure token is from @BotFather
3. No spaces around the token

#### "Can't find python/py command"
**Problem**: Python not in PATH
**Solutions**:
- **Windows**: Use `python` instead of `py`, or reinstall Python with "Add to PATH" option
- **Linux/macOS**: Install Python 3 or use `python` instead of `python3`

#### "Permission denied" (Linux/macOS)
**Problem**: Script not executable
**Solution**:
```bash
chmod +x setup.sh
chmod +x bot.py
```

#### "Session errors"
**Problem**: Authentication issues
**Solution**:
1. Delete any `.session` files
2. Restart the bot
3. Re-authenticate when prompted

### Debug Mode

Enable detailed logging by adding to `.env`:
```env
DEBUG_MODE=true
```

### Check Bot Status

Use the `/status` command in your bot to verify:
- Current settings
- Bot version
- Export statistics

## 🔄 Updating

To update to a new version:

1. **Backup your configuration**:
   ```bash
   cp .env .env.backup
   ```

2. **Pull updates** (if using Git):
   ```bash
   git pull
   ```

3. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Restart the bot**

## 🐳 Docker Setup (Advanced)

For containerized deployment:

1. **Create Dockerfile** (not included in this version)
2. **Build image**:
   ```bash
   docker build -t telegram-export-bot .
   ```
3. **Run container**:
   ```bash
   docker run -d --env-file .env telegram-export-bot
   ```

## 📱 Virtual Environment Setup (Recommended)

For isolated Python environment:

### Windows
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔐 Security Considerations

1. **Keep credentials secure**:
   - Never share your `.env` file
   - Use environment variables in production
   - Regular token rotation

2. **File permissions**:
   ```bash
   chmod 600 .env  # Linux/macOS only
   ```

3. **Network security**:
   - Use HTTPS proxies if required
   - Consider firewall settings

## 📞 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review error messages** carefully
3. **Enable debug mode** for detailed logs
4. **Check dependencies** are properly installed
5. **Verify configuration** is correct

For additional support, check the main README.md file.