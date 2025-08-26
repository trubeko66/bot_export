@echo off
REM Скрипт для автоматизации авторизации Telegram в Docker контейнере (Updated)
REM Использование: docker-auth-new.bat

setlocal EnableDelayedExpansion

echo 🤖 Telegram Bot Docker Authorization Script (Updated)
echo ==================================================

REM Проверяем что Docker доступен
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен или недоступен!
    pause
    exit /b 1
)

REM Проверяем что файл .env существует
if not exist ".env" (
    echo ❌ Файл .env не найден!
    echo    Скопируйте .env.template в .env и заполните настройки:
    echo    copy .env.template .env
    pause
    exit /b 1
)

REM Загружаем переменные из .env (упрощенная версия)
for /f "usebackq tokens=1,2 delims==" %%A in (".env") do (
    if "%%A"=="PHONE_NUMBER" set PHONE_NUMBER=%%B
    if "%%A"=="BOT_TOKEN" set BOT_TOKEN=%%B
    if "%%A"=="API_ID" set API_ID=%%B
    if "%%A"=="API_HASH" set API_HASH=%%B
    if "%%A"=="CLOUD_PASSWORD" set CLOUD_PASSWORD=%%B
)

REM Проверяем обязательные переменные
if "%BOT_TOKEN%"=="" (
    echo ❌ BOT_TOKEN не задан в .env файле!
    pause
    exit /b 1
)
if "%API_ID%"=="" (
    echo ❌ API_ID не задан в .env файле!
    pause
    exit /b 1
)
if "%API_HASH%"=="" (
    echo ❌ API_HASH не задан в .env файле!
    pause
    exit /b 1
)
if "%PHONE_NUMBER%"=="" (
    echo ❌ PHONE_NUMBER не задан в .env файле!
    pause
    exit /b 1
)

echo 📱 Номер телефона: %PHONE_NUMBER%
echo.

echo 🐳 Запуск Docker контейнера для авторизации...
docker compose up -d

echo ⏳ Ожидание запуска контейнера...
timeout /t 5 /nobreak > nul

REM Проверяем статус контейнера
docker compose ps | findstr "running" >nul
if errorlevel 1 (
    echo ❌ Контейнер не запустился!
    echo Проверьте логи: docker compose logs
    pause
    exit /b 1
)

echo.
echo 📱 Telegram отправит код подтверждения на номер %PHONE_NUMBER%
echo    Введите код когда получите SMS/уведомление:
set /p telegram_code="Код подтверждения: "

if "%telegram_code%"=="" (
    echo ❌ Код не введен!
    pause
    exit /b 1
)

echo 🔐 Устанавливаю код подтверждения и запускаю авторизацию...

REM Запускаем авторизацию с кодом
docker compose exec -e TELEGRAM_CODE=%telegram_code% telegram-bot python auto_auth.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ Авторизация завершена успешно!
    echo 📝 Сессия сохранена в data/bot_session.session
    echo.
    echo 🚀 Теперь можно запустить бота обычным способом:
    echo    docker compose up -d
    echo.
    echo 📋 Управление контейнером:
    echo    Остановить: docker compose down
    echo    Логи:      docker compose logs -f
    echo    Статус:    docker compose ps
) else (
    echo.
    echo ❌ Ошибка авторизации!
    echo 📋 Проверьте логи: docker compose logs telegram-bot
    echo 🔄 Попробуйте снова или свяжитесь с поддержкой
    pause
    exit /b 1
)

echo.
echo 🛑 Остановка временного контейнера...
docker compose down

echo.
pause