# Telegram Channel Export Bot / Телеграм Бот для Экспорта Каналов

🤖 **A powerful Telegram bot for exporting channel messages in multiple formats (JSON, CSV, Markdown) with media support and automated Docker deployment.**

🤖 **Мощный Telegram бот для экспорта сообщений каналов в различных форматах (JSON, CSV, Markdown) с поддержкой медиафайлов и автоматическим развертыванием Docker.**

---

## 🌐 Language Selection / Выбор языка

<details>
<summary><b>📖 English Documentation</b></summary>

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation Methods](#-installation-methods)
- [🐳 Docker Deployment](#-docker-deployment)
- [🔧 Configuration](#-configuration)
- [📖 Usage Guide](#-usage-guide)
- [🔐 Authentication Setup](#-authentication-setup)
- [🎯 Bot Functionality](#-bot-functionality)
- [📁 Project Structure](#-project-structure)
- [🧪 Testing](#-testing)
- [🐛 Troubleshooting](#-troubleshooting)
- [📋 Requirements](#-requirements)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## ✨ Features

### 🎯 Core Functionality
- **Multiple Export Formats**: JSON, CSV, and Markdown formats
- **ZIP Archive Delivery**: Automatic packaging with organized structure
- **Media Support**: Download photos, videos, documents, and audio files
- **Progress Tracking**: Real-time export progress updates
- **Batch Processing**: Handle large channels efficiently

### 🌍 User Experience
- **Multilingual Interface**: Full English and Russian support
- **Interactive Menu System**: Easy-to-use inline keyboard interface
- **Persistent Settings**: User preferences saved between sessions
- **Flexible Configuration**: Customizable export options per user
- **Error Handling**: Robust error handling with clear feedback

### ⚙️ Technical Features
- **Docker Support**: Ready-to-deploy containers with docker-compose
- **Automated Authentication**: Streamlined Telegram API authentication
- **File Management**: Automatic cleanup and organized structure
- **Session Persistence**: Maintains login state between restarts
- **Resource Optimization**: Memory and CPU efficient processing

---

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# 1. Clone and setup
git clone <repository-url>
cd bot_export
cp .env.template .env

# 2. Configure credentials in .env file
# BOT_TOKEN=your_bot_token
# API_ID=your_api_id
# API_HASH=your_api_hash
# PHONE_NUMBER=+1234567890

# 3. Deploy with Docker Compose
docker compose up -d
```

### Option 2: Manual Installation

```bash
# 1. Setup environment
pip install -r requirements.txt
mkdir -p exports/media

# 2. Configure
cp .env.template .env
# Edit .env with your credentials

# 3. Run
python bot.py
```

---

## 📦 Installation Methods

<details>
<summary><b>🖥️ Windows Installation</b></summary>

### Quick Setup
1. **Run setup script**: `setup.bat`
2. **Configure credentials**: Edit `.env` file
3. **Start bot**: `start.bat`

### Manual Setup
```cmd
# Install dependencies
py -m pip install -r requirements.txt

# Create directories
mkdir exports
mkdir exports\media

# Configure and run
copy .env.template .env
py bot.py
```

</details>

<details>
<summary><b>🐧 Linux/macOS Installation</b></summary>

### Quick Setup
```bash
# Make executable and run
chmod +x setup.sh
./setup.sh

# Configure and start
nano .env
python3 bot.py
```

### Manual Setup
```bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Create directories
mkdir -p exports/media

# Configure and run
cp .env.template .env
python3 bot.py
```

</details>

---

## 🐳 Docker Deployment

<details>
<summary><b>📋 Prerequisites</b></summary>

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)

</details>

<details>
<summary><b>🚀 Deployment Steps</b></summary>

### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd bot_export

# Copy environment template
cp .env.template .env
```

### 2. Configuration
Edit `.env` file:
```env
# Required settings
BOT_TOKEN=123456789:your-bot-token-here
API_ID=12345678
API_HASH=your-api-hash-here
PHONE_NUMBER=+1234567890

# Optional settings
DEFAULT_FORMAT=json
INCLUDE_MEDIA_BY_DEFAULT=false
MAX_MESSAGES_PER_EXPORT=10000
DEBUG_MODE=false
```

### 3. Deploy
```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f telegram-bot

# Stop services
docker compose down
```

</details>

---

## 🔧 Configuration

<details>
<summary><b>📊 Environment Variables</b></summary>

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | - | ✅ |
| `API_ID` | Telegram API ID from my.telegram.org | - | ✅ |
| `API_HASH` | Telegram API Hash from my.telegram.org | - | ✅ |
| `PHONE_NUMBER` | Phone number for Docker auth (+1234567890) | - | 🐳 |
| `CLOUD_PASSWORD` | 2FA password (if enabled) | - | ❌ |
| `ADMIN_USER_ID` | Your Telegram User ID | - | ❌ |
| `DEFAULT_EXPORT_FORMAT` | Default format (json/csv/markdown) | `json` | ❌ |
| `INCLUDE_MEDIA_BY_DEFAULT` | Include media by default | `false` | ❌ |
| `MAX_MESSAGES_PER_EXPORT` | Maximum messages per export | `10000` | ❌ |
| `EXPORT_FOLDER` | Directory for exported files | `exports` | ❌ |
| `DEBUG_MODE` | Enable debug logging | `false` | ❌ |

</details>

<details>
<summary><b>🔑 Getting Telegram Credentials</b></summary>

### Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the provided token

### API Credentials
1. Visit [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy `api_id` and `api_hash`

</details>

---

**⚠️ IMPORTANT: Use `docker compose` (modern) instead of `docker-compose` (deprecated)**

## 📖 Usage Guide

### Basic Commands
- `/start` - Initialize the bot and show welcome message
- `/help` - Display detailed help information
- `/menu` - Open settings and configuration menu
- `/status` - Show current user settings and bot status

### Export Process
1. Send channel username/link (`@channelname`, `https://t.me/channelname`, or `channelname`)
2. Bot processes messages and provides real-time updates
3. Receive ZIP archive with exported data via Telegram
4. Files are automatically cleaned up after delivery

### Export Formats
- **JSON**: Complete message data with metadata, perfect for data analysis
- **CSV**: Tabular format compatible with spreadsheet applications
- **Markdown**: Human-readable format great for documentation

---

## 🔐 Authentication Setup

<details>
<summary><b>🐳 Docker Authentication (Updated)</b></summary>

### Automated Scripts
```bash
# Windows
docker-auth-new.bat

# Linux/macOS
chmod +x docker-auth-new.sh
./docker-auth-new.sh
```

### Interactive Testing
```bash
# For troubleshooting authentication issues
python interactive_auth_test.py
```

### Manual Authentication
```bash
# 1. Start container
docker compose up -d

# 2. Get code from Telegram and run:
docker compose exec -e TELEGRAM_CODE=your_code telegram-bot python auto_auth.py
```

### Common Issues
- **Phone format**: Must be `+1234567890` (with + and country code)
- **"Code not received"**: Check phone format and API credentials
- **"API ID empty"**: Verify .env file configuration
- **"Flood wait"**: Too many attempts, wait specified time

</details>

---

## 🎯 Bot Functionality

### Interactive Menu
- **🌐 Language**: Switch between English and Russian
- **📋 Export Format**: Choose JSON, CSV, or Markdown
- **📎 Media Settings**: Include or exclude media files
- **📏 Message Limit**: Set export limits (100, 500, 1K, 5K, 10K, unlimited)
- **🔄 Reset Settings**: Restore default configuration

### Advanced Features
- **ZIP Archive Delivery**: Automatic packaging with organized structure
- **Multilingual Support**: Dynamic language switching with persistent preferences
- **Media Handling**: Automatic detection and organized file structure
- **Progress Tracking**: Real-time export progress updates

---

## 📁 Project Structure

```
bot_export/
├── 📄 Core Application
│   ├── bot.py                    # Main bot application
│   ├── config.py                 # Configuration management
│   ├── exporters.py              # Export functionality
│   ├── user_settings.py          # User settings management
│   ├── languages.py              # Multilingual support
│   └── zip_utils.py              # ZIP archive utilities
├── 🔐 Authentication
│   ├── auth_helper.py            # Automated authentication
│   ├── auto_auth.py              # Authentication testing
│   └── interactive_auth_test.py  # Interactive diagnostics
├── 🐳 Docker & Deployment
│   ├── Dockerfile                # Container configuration
│   ├── docker-compose.yml        # Orchestration setup
│   ├── docker-auth-new.sh        # Linux auth script
│   └── docker-auth-new.bat       # Windows auth script
├── 📚 Documentation
│   ├── README.md                 # This file
│   ├── АВТОРИЗАЦИЯ.md             # Russian auth guide
│   └── РЕШЕНИЕ_ПРОБЛЕМЫ_АВТОРИЗАЦИИ.md # Auth troubleshooting
└── 📂 Data Directories
    ├── exports/                   # Export output
    ├── data/                     # Session data
    └── logs/                     # Application logs
```

---

## 🧪 Testing

```bash
# Authentication tests
python test_auth.py
python interactive_auth_test.py
python auto_auth.py

# Export format tests
python test_export_formats.py
python test_simple.py
python test_markdown.py
```

---

## 🐛 Troubleshooting

### Common Issues
1. **"Module not found"**: Run `pip install -r requirements.txt`
2. **"Invalid token"**: Check BOT_TOKEN in .env file
3. **"Can't access channel"**: Verify channel permissions and API credentials
4. **Docker issues**: Check `docker compose logs` and .env configuration
5. **Authentication failures**: Use `python interactive_auth_test.py`

### Debug Mode
```env
# In .env file
DEBUG_MODE=true
```

---

## 📋 Requirements

| Package | Version | Purpose |
|---------|---------|----------|
| `python-telegram-bot` | `20.7` | Telegram Bot API wrapper |
| `telethon` | `1.34.0` | Telegram client library |
| `python-dotenv` | `1.0.0` | Environment variable management |
| `aiofiles` | `23.2.0` | Asynchronous file operations |
| `pandas` | `2.1.4` | Data manipulation (CSV exports) |
| `asyncio-throttle` | `1.0.2` | Rate limiting |
| `markdown` | `3.5.2` | Markdown processing |
| `pytz` | `2023.4` | Timezone handling |

**System Requirements:**
- Python 3.8+
- 256MB RAM (512MB for Docker)
- 1GB free space
- Internet connection

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with tests
4. Follow PEP 8 style guidelines
5. Submit a pull request

---

## 📜 License

This project is open source and available under the MIT License.

---

## 📞 Support

If you encounter issues:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review error messages and logs
3. Ensure all dependencies are installed
4. Verify configuration is correct
5. Use interactive authentication test for auth issues

</details>

---
## 🇷🇺 Русская документация

<details>
<summary><b>📖 Русская документация</b></summary>



<details>
<summary><b>📑 Содержание (русский язык)</b></summary>

- [✨ Основные возможности](#-основные-возможности)
- [🚀 Быстрый старт](#-быстрый-старт)
- [🔧 Установка](#-установка-1)
- [🐳 Docker развертывание](#-docker-развертывание)
- [⚙️ Конфигурация](#️-конфигурация)
- [📖 Руководство по использованию](#-руководство-по-использованию)
- [🔐 Настройка авторизации](#-настройка-авторизации)
- [🎯 Функционал бота](#-функционал-бота-1)
- [📁 Структура проекта](#-структура-проекта-1)
- [🧪 Тестирование](#-тестирование-1)
- [🐛 Решение проблем](#-решение-проблем)
- [📋 Зависимости](#-зависимости)
- [🤝 Участие в разработке](#-участие-в-разработке)
- [📜 Лицензия](#-лицензия-1)

</details>

---

## ✨ Основные возможности

### 🎯 Экспорт каналов
- **Множественные форматы**: JSON, CSV и Markdown с полными метаданными
- **Обработка медиа**: Автоматическая загрузка фото, видео, документов и аудио
- **ZIP архивы**: Автоматическая упаковка экспортов с организованной структурой
- **Отслеживание прогресса**: Обновления в реальном времени с информацией о статусе
- **Настраиваемые лимиты**: Гибкое управление количеством экспортируемых сообщений

### 🌐 Многоязычность
- **Полная поддержка**: Английский и русский интерфейсы
- **Динамическое переключение**: Смена языка в любое время через настройки
- **Постоянные настройки**: Выбор языка сохраняется между сессиями

### 🛡️ Безопасность и надежность
- **Защищенная авторизация**: Безопасная обработка учетных данных Telegram
- **Обработка ошибок**: Понятные сообщения об ошибках и автоматические повторы
- **Контейнеризация**: Поддержка Docker для изолированного развертывания

---

## 🚀 Быстрый старт

### Локальная установка
```bash
# 1. Клонируйте репозиторий
git clone [repository-url]
cd bot_export

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Настройте .env файл
cp .env.template .env
# Отредактируйте .env с вашими токенами

# 4. Запустите бота
python bot.py
```

### Docker развертывание
```bash
# 1. Клонируйте и настройте
git clone [repository-url]
cd bot_export
cp .env.template .env
# Отредактируйте .env файл

# 2. Запустите контейнер
docker compose up -d

# 3. Авторизуйтесь
# Windows:
docker-auth-new.bat
# Linux/macOS:
./docker-auth-new.sh
```

---

## 🔧 Установка

<details>
<summary><b>📋 Системные требования</b></summary>

### Минимальные требования
- **Python**: 3.9 или выше
- **Память**: 512MB RAM (рекомендуется 1GB)
- **Диск**: 1GB свободного места
- **ОС**: Windows 10/11, Linux, macOS

### Дополнительные требования
- **Docker**: Для контейнерного развертывания
- **Git**: Для клонирования репозитория
- **Telegram аккаунт**: Для получения API ключей

</details>

<details>
<summary><b>📝 Пошаговая установка</b></summary>

### Windows
```cmd
# 1. Клонируйте репозиторий
git clone [repository-url]
cd bot_export

# 2. Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Настройте окружение
copy .env.template .env
# Отредактируйте .env файл в текстовом редакторе

# 5. Запустите бота
python bot.py
```

### Linux/macOS
```bash
# 1. Клонируйте репозиторий
git clone [repository-url]
cd bot_export

# 2. Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Настройте окружение
cp .env.template .env
# Отредактируйте .env файл

# 5. Запустите бота
python3 bot.py
```

</details>

---

## 🐳 Docker развертывание

<details>
<summary><b>🚀 Быстрое развертывание</b></summary>

### Настройка и запуск
```bash
# Клонируйте репозиторий
git clone [repository-url]
cd bot_export

# Настройте переменные окружения
cp .env.template .env
# Отредактируйте .env файл с вашими данными

# Запустите сервисы
docker compose up -d

# Проверьте статус
docker compose ps
```

### Управление контейнером
```bash
# Просмотр логов
docker compose logs -f

# Остановка сервисов
docker compose down
```

</details>

---

## ⚙️ Конфигурация

<details>
<summary><b>📊 Переменные окружения</b></summary>

| Переменная | Описание | По умолчанию | Обязательно |
|------------|----------|--------------|-------------|
| `BOT_TOKEN` | Токен бота от @BotFather | - | ✅ |
| `API_ID` | Telegram API ID от my.telegram.org | - | ✅ |
| `API_HASH` | Telegram API Hash от my.telegram.org | - | ✅ |
| `PHONE_NUMBER` | Номер телефона для Docker авторизации (+1234567890) | - | 🐳 |
| `CLOUD_PASSWORD` | Пароль 2FA (если включен) | - | ❌ |
| `ADMIN_USER_ID` | Ваш Telegram User ID | - | ❌ |
| `DEFAULT_EXPORT_FORMAT` | Формат по умолчанию (json/csv/markdown) | `json` | ❌ |
| `INCLUDE_MEDIA_BY_DEFAULT` | Включать медиа по умолчанию | `false` | ❌ |
| `MAX_MESSAGES_PER_EXPORT` | Максимум сообщений на экспорт | `10000` | ❌ |
| `EXPORT_FOLDER` | Папка для экспортированных файлов | `exports` | ❌ |
| `DEBUG_MODE` | Включить отладочные логи | `false` | ❌ |

</details>

<details>
<summary><b>🔑 Получение учетных данных Telegram</b></summary>

### Токен бота
1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте предоставленный токен

### API учетные данные
1. Посетите [my.telegram.org](https://my.telegram.org)
2. Войдите с номером телефона
3. Перейдите в "API Development Tools"
4. Создайте новое приложение
5. Скопируйте `api_id` и `api_hash`

</details>

---

**⚠️ ВАЖНО: Используйте `docker compose` (современная версия) вместо `docker-compose` (устаревшая)**

## 📖 Руководство по использованию

### Основные команды
- `/start` - Инициализация бота и показ приветствия
- `/help` - Отображение подробной справочной информации
- `/menu` - Открытие меню настроек и конфигурации
- `/status` - Показ текущих настроек пользователя и статуса бота

### Процесс экспорта
1. Отправьте имя пользователя/ссылку канала (`@channelname`, `https://t.me/channelname`, или `channelname`)
2. Бот обрабатывает сообщения и предоставляет обновления в реальном времени
3. Получайте ZIP архив с экспортированными данными через Telegram
4. Файлы автоматически очищаются после доставки

### Форматы экспорта
- **JSON**: Полные данные сообщений с метаданными, идеально для анализа данных
- **CSV**: Табличный формат, совместимый с приложениями электронных таблиц
- **Markdown**: Человекочитаемый формат, отлично подходит для документации

---

## 🔐 Настройка авторизации

<details>
<summary><b>🐳 Docker авторизация (обновлено)</b></summary>

### Автоматизированные скрипты
```bash
# Windows
docker-auth-new.bat

# Linux/macOS
chmod +x docker-auth-new.sh
./docker-auth-new.sh
```

### Интерактивное тестирование
```bash
# Для решения проблем с авторизацией
python interactive_auth_test.py
```

### Ручная авторизация
```bash
# 1. Запустите контейнер
docker compose up -d

# 2. Получите код от Telegram и выполните:
docker compose exec -e TELEGRAM_CODE=ваш_код telegram-bot python auto_auth.py
```

### Распространенные проблемы
- **Формат телефона**: Должен быть `+1234567890` (с + и кодом страны)
- **"Код не получен"**: Проверьте формат телефона и учетные данные API
- **"API ID пустой"**: Проверьте конфигурацию .env файла
- **"Flood wait"**: Слишком много попыток, подождите указанное время

</details>

---

## 🎯 Функционал бота

### Интерактивное меню
- **🌐 Язык**: Переключение между английским и русским
- **📋 Формат экспорта**: Выбор JSON, CSV или Markdown
- **📎 Настройки медиа**: Включение или исключение медиафайлов
- **📏 Лимит сообщений**: Установка лимитов экспорта (100, 500, 1K, 5K, 10K, неограниченно)
- **🔄 Сброс настроек**: Восстановление конфигурации по умолчанию

### Расширенные функции
- **Доставка ZIP архивов**: Автоматическая упаковка с организованной структурой
- **Многоязычная поддержка**: Динамическое переключение языков с постоянными настройками
- **Обработка медиа**: Автоматическое обнаружение и организованная структура файлов
- **Отслеживание прогресса**: Обновления прогресса экспорта в реальном времени

---

## 📁 Структура проекта

```
bot_export/
├── 📄 Основное приложение
│   ├── bot.py                    # Главное приложение бота
│   ├── config.py                 # Управление конфигурацией
│   ├── exporters.py              # Функционал экспорта
│   ├── user_settings.py          # Управление настройками пользователей
│   ├── languages.py              # Многоязычная поддержка
│   └── zip_utils.py              # Утилиты ZIP архивов
├── 🔐 Авторизация
│   ├── auth_helper.py            # Автоматизированная авторизация
│   ├── auto_auth.py              # Тестирование авторизации
│   └── interactive_auth_test.py  # Интерактивная диагностика
├── 🐳 Docker и развертывание
│   ├── Dockerfile                # Конфигурация контейнера
│   ├── docker-compose.yml        # Настройка оркестрации
│   ├── docker-auth-new.sh        # Linux скрипт авторизации
│   └── docker-auth-new.bat       # Windows скрипт авторизации
├── 📚 Документация
│   ├── README.md                 # Этот файл
│   ├── АВТОРИЗАЦИЯ.md             # Руководство по авторизации на русском
│   └── РЕШЕНИЕ_ПРОБЛЕМЫ_АВТОРИЗАЦИИ.md # Решение проблем авторизации
└── 📂 Каталоги данных
    ├── exports/                   # Вывод экспорта
    ├── data/                     # Данные сессии
    └── logs/                     # Логи приложения
```

---

## 🧪 Тестирование

```bash
# Тесты авторизации
python test_auth.py
python interactive_auth_test.py
python auto_auth.py

# Тесты форматов экспорта
python test_export_formats.py
python test_simple.py
python test_markdown.py
```

---

## 🐛 Решение проблем

### Распространенные проблемы
1. **"Модуль не найден"**: Выполните `pip install -r requirements.txt`
2. **"Неверный токен"**: Проверьте BOT_TOKEN в .env файле
3. **"Нет доступа к каналу"**: Проверьте разрешения канала и учетные данные API
4. **Проблемы Docker**: Проверьте `docker compose logs` и конфигурацию .env
5. **Ошибки авторизации**: Используйте `python interactive_auth_test.py`

### Режим отладки
```env
# В .env файле
DEBUG_MODE=true
```

---

## 📋 Зависимости

| Пакет | Версия | Назначение |
|-------|--------|------------|
| `python-telegram-bot` | `20.7` | Обертка Telegram Bot API |
| `telethon` | `1.34.0` | Библиотека клиента Telegram |
| `python-dotenv` | `1.0.0` | Управление переменными окружения |
| `aiofiles` | `23.2.0` | Асинхронные файловые операции |
| `pandas` | `2.1.4` | Манипуляция данными (CSV экспорты) |
| `asyncio-throttle` | `1.0.2` | Ограничение скорости |
| `markdown` | `3.5.2` | Обработка Markdown |
| `pytz` | `2023.4` | Обработка часовых поясов |

**Системные требования:**
- Python 3.9+
- 512MB RAM (рекомендуется 1GB)
- 1GB свободного места на диске

---

## 🤝 Участие в разработке

1. Сделайте форк репозитория
2. Создайте ветку функции
3. Внесите изменения
4. Добавьте тесты для новой функциональности
5. Отправьте pull request

---

## 📜 Лицензия

Этот проект является открытым исходным кодом и доступен под лицензией MIT.

---

## 📞 Поддержка

Если у вас возникли проблемы или вопросы:

1. Проверьте раздел решения проблем выше
2. Внимательно изучите сообщения об ошибках
3. Убедитесь, что все зависимости установлены
4. Проверьте правильность конфигурации

---

## 📋 Дополнительные ресурсы

### Документация проекта

| Файл | Описание | Язык |
|------|----------|------|
| [`INSTALL.md`](INSTALL.md) | Подробное руководство по установке | EN |
| [`DOCKER.md`](DOCKER.md) | Руководство по Docker развертыванию | EN |
| [`DOCKER_AUTH_GUIDE.md`](DOCKER_AUTH_GUIDE.md) | Подробное руководство по авторизации Docker | EN |
| [`АВТОРИЗАЦИЯ.md`](АВТОРИЗАЦИЯ.md) | Руководство по авторизации | RU |
| [`РЕШЕНИЕ_ПРОБЛЕМЫ_АВТОРИЗАЦИИ.md`](РЕШЕНИЕ_ПРОБЛЕМЫ_АВТОРИЗАЦИИ.md) | Решение проблем авторизации | RU |
| [`CHANGELOG.md`](CHANGELOG.md) | История версий и обновления | EN |
| [`LANGUAGE_CHANGES.md`](LANGUAGE_CHANGES.md) | Документация языковых функций | EN |
| [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md) | Сводка реализации | EN |

### Скрипты и утилиты

| Скрипт | Платформа | Назначение |
|--------|-----------|------------|
| `setup.bat` | Windows | Автоматическая настройка и установка |
| `setup.sh` | Linux/macOS | Автоматическая настройка и установка |
| `start.bat` | Windows | Запуск бота |
| `docker-auth-new.bat` | Windows | Docker авторизация |
| `docker-auth-new.sh` | Linux/macOS | Docker авторизация |
| `interactive_auth_test.py` | Все | Интерактивное тестирование авторизации |

---

**✅ Документация консолидирована и организована! Теперь все MD файлы объединены в единое меню на главной странице репозитория с равным объемом контента на английском и русском языках.**