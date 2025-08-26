#!/bin/bash

# Скрипт для автоматизации авторизации Telegram в Docker контейнере
# Использование: ./docker-auth.sh

set -e

echo "🤖 Telegram Bot Docker Authorization Script"
echo "=========================================="

# Проверяем что файл .env существует
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "   Скопируйте .env.template в .env и заполните настройки:"
    echo "   cp .env.template .env"
    exit 1
fi

# Загружаем переменные из .env
source .env

# Проверяем обязательные переменные
if [ -z "$BOT_TOKEN" ] || [ -z "$API_ID" ] || [ -z "$API_HASH" ] || [ -z "$PHONE_NUMBER" ]; then
    echo "❌ Не заполнены обязательные переменные в .env файле!"
    echo "   Требуются: BOT_TOKEN, API_ID, API_HASH, PHONE_NUMBER"
    exit 1
fi

echo "📱 Номер телефона: $PHONE_NUMBER"
echo ""

# Функция для остановки контейнера
cleanup() {
    echo "🛑 Остановка контейнера..."
    docker-compose down > /dev/null 2>&1 || true
}

# Регистрируем функцию очистки при выходе
trap cleanup EXIT

echo "🐳 Запуск Docker контейнера для авторизации..."
docker-compose up -d

echo "⏳ Ожидание запуска контейнера..."
sleep 5

echo ""
echo "📱 Telegram отправит код подтверждения на номер $PHONE_NUMBER"
echo "   Введите код когда получите SMS/уведомление:"
read -p "Код подтверждения: " telegram_code

if [ -z "$telegram_code" ]; then
    echo "❌ Код не введен!"
    exit 1
fi

echo "🔐 Устанавливаю код подтверждения..."
docker-compose exec telegram-bot bash -c "export TELEGRAM_CODE=$telegram_code && python bot.py" &

# Даем время на авторизацию
sleep 10

# Если требуется облачный пароль
if [ ! -z "$CLOUD_PASSWORD" ]; then
    echo "🔒 Используется облачный пароль для 2FA..."
fi

echo ""
echo "✅ Авторизация завершена!"
echo "📝 Сессия сохранена в data/bot_session.session"
echo ""
echo "🚀 Теперь можно запустить бота обычным способом:"
echo "   docker-compose up -d"
echo ""
echo "📋 Управление контейнером:"
echo "   Остановить: docker-compose down"
echo "   Логи:      docker-compose logs -f"
echo "   Статус:    docker-compose ps"