# Telegram Bot Authentication Guide / Руководство по авторизации Telegram Bot

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [⚙️ Environment Setup](#️-environment-setup)
- [🔑 Getting Credentials](#-getting-credentials)
- [🐳 Docker Authentication](#-docker-authentication)
- [💻 Local Authentication](#-local-authentication)
- [🧪 Testing](#-testing)
- [🚨 Troubleshooting](#-troubleshooting)
- [📞 Support](#-support)

---

## 🚀 Quick Start

### 1. Setup
```bash
# Copy environment template
cp .env.template .env

# Fill in .env file:
BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+1234567890  # MUST include + and country code!
CLOUD_PASSWORD=your_2fa_password  # if 2FA is enabled
```

### 2. Authentication

**Windows (updated for docker compose):**
```cmd
docker-auth-new.bat
```

**Linux/macOS (updated for docker compose):**
```bash
chmod +x docker-auth-new.sh
./docker-auth-new.sh
```

**Interactive testing (for code issues):**
```bash
# Diagnostics and interactive authorization
python interactive_auth_test.py
```

**Manual authorization:**
```bash
# 1. Start container
docker compose up -d

# 2. Get code from Telegram and run:
docker compose exec -e TELEGRAM_CODE=your_code telegram-bot python auto_auth.py
```

### 3. Start Bot
```bash
docker compose up -d
```

---

## ⚙️ Environment Setup

### Environment Variables

Required variables in `.env` file:

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Bot token from @BotFather | `123456789:ABC...` | ✅ |
| `API_ID` | API ID from my.telegram.org | `12345678` | ✅ |
| `API_HASH` | API Hash from my.telegram.org | `abcdef123...` | ✅ |
| `PHONE_NUMBER` | Phone number (international format) | `+1234567890` | 🐳 Docker |
| `CLOUD_PASSWORD` | 2FA password (if enabled) | `mypassword` | ❌ |
| `TELEGRAM_CODE` | Confirmation code from Telegram | `12345` | ⚡ Temporary |
| `CODE_WAIT_TIMEOUT` | Code wait timeout (seconds) | `60` | ❌ |

---

## 🔑 Getting Credentials

### Bot Token (@BotFather)

1. Open Telegram and find [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name for your bot
   - Choose a username (must end with 'bot')
4. Copy the provided token

### API Credentials (my.telegram.org)

1. Visit [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application:
   - **App title**: "Channel Export Bot"
   - **Short name**: "export_bot"
   - **Platform**: Other
5. Copy `api_id` and `api_hash`

---

## 🐳 Docker Authentication

### Automated Scripts (Recommended)

**Windows:**
```cmd
docker-auth-new.bat
```

**Linux/macOS:**
```bash
chmod +x docker-auth-new.sh
./docker-auth-new.sh
```

### Manual Docker Authorization

```bash
# 1. Start container
docker compose up -d

# 2. Get confirmation code from Telegram
# 3. Run authorization with code:
docker compose exec -e TELEGRAM_CODE=12345 telegram-bot python auto_auth.py

# 4. If 2FA is required:
docker compose exec -e CLOUD_PASSWORD=your_password telegram-bot python auto_auth.py
```

### Interactive Docker Authorization

```bash
# Connect for interactive authorization
docker compose exec telegram-bot python interactive_auth_test.py
```

---

## 💻 Local Authentication

### Automatic Authorization

```bash
# Set environment variables
export PHONE_NUMBER="+1234567890"
export TELEGRAM_CODE="12345"  # Get from Telegram
export CLOUD_PASSWORD="password"  # If 2FA is enabled

# Run authorization
python auto_auth.py
```

### Interactive Authorization

```bash
# Interactive testing and authorization
python interactive_auth_test.py
```

---

## 🧪 Testing

### Authentication Tests

```bash
# Check authorization system
python test_auth.py

# Interactive diagnostics
python interactive_auth_test.py

# Test automatic authorization
python auto_auth.py
```

### Export Tests

```bash
# Test export formats
python test_export_formats.py
python test_simple.py
python test_markdown.py
```

---

## 🚨 Troubleshooting

### Common Errors and Solutions

#### "Confirmation code not received"

**Causes and solutions:**

1. **Incorrect phone number format**
   - ✅ Correct: `+1234567890`
   - ❌ Incorrect: `1234567890`, `1-234-567-890`

2. **Invalid API credentials**
   - Get new credentials from [my.telegram.org](https://my.telegram.org)
   - Ensure API_ID and API_HASH are correctly copied

3. **Environment variable issues**
   - Check `.env` file for extra spaces
   - Ensure no quotes around values

#### "API ID or Hash cannot be empty"

```bash
# Check .env file contents
cat .env  # Linux/macOS
type .env  # Windows

# Ensure file contains:
API_ID=12345678
API_HASH=abcdef1234567890
```

#### "Invalid phone number"

- Number must start with `+` and country code
- For USA: `+1`, for UK: `+44`, for Russia: `+7`
- Don't use spaces, dashes, or parentheses

#### "Phone code expired"

- Code is valid for only 5 minutes
- Request a new code and enter faster
- Use interactive authorization for better control

#### "Phone code invalid"

- Enter only digits without spaces
- Ensure code is sent to the correct number
- Verify the number in `.env` matches your Telegram number

#### "Flood wait"

- Too many authorization attempts in a row
- Wait the specified time before trying again
- Use `interactive_auth_test.py` for diagnostics

### Diagnostic Commands

```bash
# Check Docker status
docker compose ps

# View container logs
docker compose logs telegram-bot

# Check environment variables in container
docker compose exec telegram-bot env | grep -E "API_|BOT_|PHONE"

# Stop container
docker compose down

# Remove old session for re-authorization
rm bot_session.session   # Linux/macOS
del bot_session.session  # Windows
```

### Docker Management

```bash
# Service status
docker compose ps

# Real-time logs
docker compose logs -f

# Stop all services
docker compose down

# Restart bot
docker compose restart telegram-bot

# Complete rebuild
docker compose up -d --build
```

---

## 📞 Support

### Self-Diagnostics

1. **Check environment variables** in `.env` file
2. **Verify phone number format** is international
3. **Try interactive authorization** `interactive_auth_test.py`
4. **Check logs** for detailed error information

### Checklist

- [ ] `.env` file exists and is properly filled
- [ ] Phone number is in international format with `+`
- [ ] API_ID and API_HASH obtained from [my.telegram.org](https://my.telegram.org)
- [ ] BOT_TOKEN obtained from [@BotFather](https://t.me/BotFather)
- [ ] Confirmation code arrives at the specified number
- [ ] Docker container is running (for Docker authorization)

### Useful Files

- `auth_helper.py` - automatic authorization (updated)
- `auto_auth.py` - test authorization  
- `docker-auth-new.sh/bat` - new scripts for docker compose
- `interactive_auth_test.py` - interactive diagnostics
- `test_auth.py` - system testing

---

**⚠️ IMPORTANT: Use `docker compose` (modern) command instead of `docker-compose` (deprecated)**

**💡 Tip**: The confirmation code should arrive at the phone number specified in the `PHONE_NUMBER` variable in the `.env` file.