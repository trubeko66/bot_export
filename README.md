# Telegram Channel Export Bot / Телеграм Бот для Экспорта Каналов

🤖 A powerful Telegram bot for exporting channel messages in multiple formats (JSON, CSV, Markdown) with media support.

🤖 Мощный Telegram бот для экспорта сообщений каналов в различных форматах (JSON, CSV, Markdown) с поддержкой медиафайлов.

---

## 🌐 Language / Язык

- [English Documentation](#english-documentation)
- [Русская документация](#русская-документация)

---

## English Documentation

## ✨ Features

- **Multiple Export Formats**: JSON, CSV, and Markdown
- **Media Support**: Download photos, videos, documents, and audio files
- **Interactive Menu**: Easy-to-use inline keyboard interface
- **Flexible Settings**: Customizable export options per user
- **Progress Tracking**: Real-time export progress updates
- **File Management**: Automatic cleanup and organized file structure
- **Error Handling**: Robust error handling and user feedback

## 🎯 Bot Functionality

### Core Features
1. **Channel Export**: Send any Telegram channel username/link to export its content
2. **Format Selection**: Choose between JSON, CSV, or Markdown formats
3. **Media Options**: Include or exclude media files in exports
4. **Message Limits**: Set maximum number of messages to export
5. **Settings Persistence**: User preferences are saved between sessions
6. **Progress Updates**: Real-time status updates during export process

### Export Formats

#### JSON Format
- Complete message data with metadata
- Channel information and statistics
- Structured format perfect for data analysis
- Includes all message properties and media information

#### CSV Format
- Tabular format compatible with spreadsheet applications
- Easy to import into Excel, Google Sheets, etc.
- Includes essential message data in columns
- Perfect for data analysis and reporting

#### Markdown Format
- Human-readable text format
- Properly formatted with headers and sections
- Includes channel information and message statistics
- Great for documentation and sharing

### Menu System

The bot features an intuitive menu system:

- **📋 Export Format**: Choose JSON, CSV, or Markdown
- **📎 Media Settings**: Include or exclude media files
- **📏 Message Limit**: Set export limits (100, 500, 1K, 5K, 10K, or unlimited)
- **🔄 Reset Settings**: Restore default configuration
- **ℹ️ Help**: Get detailed usage instructions

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Telegram API credentials (from [my.telegram.org](https://my.telegram.org))

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd bot_export
   ```

2. **Run the setup script**:
   ```bash
   setup.bat
   ```
   This will automatically install all dependencies and create necessary directories.

3. **Configure the bot**:
   ```bash
   copy .env.example .env
   ```
   Edit `.env` file with your credentials:
   ```env
   BOT_TOKEN=your_bot_token_here
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   ADMIN_USER_ID=your_user_id_here
   ```

4. **Start the bot**:
   ```bash
   py bot.py
   ```

### Manual Installation

If you prefer manual setup:

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create directories**:
   ```bash
   mkdir exports
   mkdir exports\media
   ```

3. **Configure environment** (see step 3 above)

4. **Run the bot** (see step 4 above)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | ✅ |
| `API_ID` | Telegram API ID from my.telegram.org | ✅ |
| `API_HASH` | Telegram API Hash from my.telegram.org | ✅ |
| `ADMIN_USER_ID` | Your Telegram User ID (optional) | ❌ |
| `DEFAULT_EXPORT_FORMAT` | Default export format (json/csv/markdown) | ❌ |
| `INCLUDE_MEDIA_BY_DEFAULT` | Include media by default (true/false) | ❌ |
| `MAX_MESSAGES_PER_EXPORT` | Default message limit | ❌ |
| `EXPORT_FOLDER` | Directory for exported files | ❌ |
| `DEBUG_MODE` | Enable debug logging (true/false) | ❌ |

### Getting Telegram Credentials

1. **Bot Token**:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` command
   - Follow instructions to create your bot
   - Copy the provided token

2. **API Credentials**:
   - Visit [my.telegram.org](https://my.telegram.org)
   - Log in with your phone number
   - Go to "API Development Tools"
   - Create a new application
   - Copy `api_id` and `api_hash`

## 📖 Usage

### Basic Usage

1. **Start the bot**: Send `/start` to your bot
2. **Configure settings**: Use `/menu` to access settings
3. **Export a channel**: Send a channel username or link:
   - `@channelname`
   - `https://t.me/channelname`
   - `channelname`

### Available Commands

- `/start` - Initialize the bot and show welcome message
- `/help` - Display detailed help information
- `/menu` - Open settings and configuration menu
- `/status` - Show current user settings and bot status

### Export Process

1. **Send channel**: Provide channel username/link
2. **Processing**: Bot fetches messages and processes data
3. **Progress updates**: Real-time status updates
4. **File delivery**: Receive exported file via Telegram
5. **Automatic cleanup**: Files are cleaned up after delivery

### Supported Channel Formats

- `@channelname` - Standard username format
- `https://t.me/channelname` - Full Telegram link
- `channelname` - Username without @ symbol

## 📁 Project Structure

```
bot_export/
├── bot.py              # Main bot application
├── config.py           # Configuration management
├── exporters.py        # Export functionality
├── user_settings.py    # User settings management
├── requirements.txt    # Python dependencies
├── setup.bat          # Windows setup script
├── .env.example       # Environment variables template
├── README.md          # This file
├── CHANGELOG.md       # Version history
├── exports/           # Export output directory
│   └── media/        # Media files directory
└── tests/            # Test files
    ├── test_simple.py
    ├── test_markdown.py
    └── test_export_formats.py
```

## 🔍 Advanced Features

### Media Handling

- **Automatic Detection**: Identifies photos, videos, documents, and audio
- **File Organization**: Media files stored in organized directory structure
- **Size Information**: File sizes included in export metadata
- **Duration Tracking**: Video and audio duration information
- **Format Preservation**: Original file formats maintained

### Export Customization

- **Message Limits**: Configure how many messages to export
- **Media Inclusion**: Choose whether to download media files
- **Format Selection**: Pick the most suitable export format
- **Progress Tracking**: Monitor export progress in real-time

### Error Handling

- **Invalid Channels**: Clear error messages for invalid channel names
- **Network Issues**: Automatic retry for network-related errors
- **Permission Errors**: Helpful messages for access-related issues
- **File Errors**: Graceful handling of file system issues

## 🧪 Testing

The project includes comprehensive tests:

```bash
# Test all export formats
py test_export_formats.py

# Test markdown generation
py test_simple.py

# Test with dependencies (requires installation)
py test_markdown.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📋 Requirements

- `python-telegram-bot==20.7` - Telegram Bot API wrapper
- `telethon==1.34.0` - Telegram client library
- `python-dotenv==1.0.0` - Environment variable management
- `aiofiles==23.2.0` - Asynchronous file operations
- `pandas==2.1.4` - Data manipulation (for CSV exports)
- `asyncio-throttle==1.0.2` - Rate limiting
- `markdown==3.5.2` - Markdown processing
- `pytz==2023.4` - Timezone handling

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Run `pip install -r requirements.txt`
   - Ensure you're using the correct Python version

2. **"Invalid token" errors**:
   - Check your BOT_TOKEN in .env file
   - Ensure token is from @BotFather

3. **"Can't access channel" errors**:
   - Verify channel username is correct
   - Ensure channel is public or bot has access
   - Check API credentials (API_ID and API_HASH)

4. **"Session file" errors**:
   - Delete bot_session.session file and restart
   - Re-authenticate with Telegram

### Debug Mode

Enable debug mode for detailed logging:
```env
DEBUG_MODE=true
```

## 📜 License

This project is open source and available under the MIT License.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the error messages carefully
3. Ensure all dependencies are installed
4. Verify your configuration is correct

## 🔄 Updates

To update the bot:

1. Pull latest changes from repository
2. Run setup script again if new dependencies were added
3. Restart the bot

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

## Русская документация

### ✨ Особенности

- **Множественные форматы экспорта**: JSON, CSV и Markdown
- **Поддержка медиа**: Загрузка фото, видео, документов и аудио
- **Интерактивное меню**: Простой в использовании интерфейс с кнопками
- **Гибкие настройки**: Настраиваемые опции экспорта для каждого пользователя
- **Отслеживание прогресса**: Обновления прогресса экспорта в реальном времени

### 🎯 Функционал бота

#### Основные возможности
1. **Экспорт каналов**: Отправьте имя пользователя/ссылку Telegram канала
2. **Выбор формата**: Выбирайте между JSON, CSV или Markdown
3. **Опции медиа**: Включайте или исключайте медиафайлы
4. **Лимит сообщений**: Устанавливайте максимальное количество сообщений

### 🚀 Установка

1. **Клонируйте репозиторий** и запустите `setup.bat` (Windows) или `setup.sh` (Linux/macOS)
2. **Настройте `.env`** файл с вашими токенами и ключами API
3. **Запустите** с помощью `start.bat` или `python3 bot.py`

### 📖 Использование

- `/start` - Старт бота
- `/menu` - Меню настроек
- `/help` - Помощь
- Отправьте `@имя_канала` для экспорта

### 🔧 Поддержка

Подробная документация на английском языке выше. См. [INSTALL.md](INSTALL.md) для детальных инструкций по установке.