#!/usr/bin/env python3
"""
Интерактивный тестер авторизации Telegram
Помогает диагностировать проблемы с получением кода подтверждения
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Добавляем путь к модулям бота
sys.path.append(str(Path(__file__).parent))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def interactive_auth_test():
    """Интерактивное тестирование авторизации"""
    try:
        from auth_helper import AutoAuth
        from config import bot_config
        
        print("🤖 Интерактивный тестер авторизации Telegram")
        print("=" * 50)
        
        # Показываем текущую конфигурацию
        print(f"📱 Номер телефона: {bot_config.phone_number}")
        print(f"🆔 API ID: {bot_config.api_id}")
        print(f"🔑 API Hash: {'*' * 10 if bot_config.api_hash else 'НЕ УСТАНОВЛЕН'}")
        print(f"🤖 Bot Token: {'*' * 10 if bot_config.bot_token else 'НЕ УСТАНОВЛЕН'}")
        
        if bot_config.password:
            print(f"🔐 Облачный пароль: установлен")
        else:
            print(f"🔐 Облачный пароль: не установлен")
        
        print()
        
        # Проверяем обязательные поля
        if not all([bot_config.phone_number, bot_config.api_id, bot_config.api_hash]):
            print("❌ Не все обязательные поля заполнены!")
            return False
        
        # Создаем тестер авторизации
        auth = AutoAuth("test_interactive_session")
        
        # Показываем инструкции
        auth.interactive_auth_prompt()
        
        # Запрашиваем подтверждение
        response = input("Продолжить тестирование авторизации? (y/N): ").strip().lower()
        if response != 'y':
            print("Тестирование отменено.")
            return True
        
        print()
        print("🚀 Начинаю интерактивную авторизацию...")
        
        # Запускаем авторизацию в интерактивном режиме
        client = await auth.create_authenticated_client(interactive=True)
        
        if await client.is_user_authorized():
            try:
                me = await client.get_me()
                name = getattr(me, 'first_name', 'Unknown')
                username = getattr(me, 'username', 'no_username')
                print(f"✅ Авторизация успешна! Пользователь: {name} (@{username})")
            except Exception as e:
                print(f"✅ Авторизация успешна! (Ошибка получения данных: {e})")
            
            # Закрываем соединение
            client.disconnect()
            
            # Удаляем тестовую сессию
            session_file = "test_interactive_session.session"
            if os.path.exists(session_file):
                os.remove(session_file)
                print(f"🗑️ Тестовая сессия удалена: {session_file}")
            
            print("\n🎉 Интерактивная авторизация работает!")
            return True
        else:
            print("❌ Авторизация не удалась")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка тестирования: {e}")
        return False

async def check_telegram_connection():
    """Проверяет подключение к Telegram API"""
    try:
        from telethon import TelegramClient
        from config import bot_config
        
        print("🔗 Проверка подключения к Telegram API...")
        
        client = TelegramClient(
            "test_connection",
            bot_config.api_id,
            bot_config.api_hash
        )
        
        await client.connect()
        
        if client.is_connected():
            print("✅ Подключение к Telegram API успешно!")
            client.disconnect()
            
            # Удаляем тестовую сессию
            session_file = "test_connection.session"
            if os.path.exists(session_file):
                os.remove(session_file)
            
            return True
        else:
            print("❌ Не удалось подключиться к Telegram API")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

async def main():
    """Основная функция"""
    print("🔍 Диагностика системы авторизации Telegram")
    print("=" * 50)
    
    # Проверка подключения
    if not await check_telegram_connection():
        print("\n💥 Проблема с подключением к Telegram API")
        print("Проверьте API_ID и API_HASH в .env файле")
        return
    
    print()
    
    # Интерактивное тестирование
    success = await interactive_auth_test()
    
    if success:
        print("\n🎉 Все тесты прошли успешно!")
        print("📋 Система авторизации готова к использованию")
        
        print("\n📋 Следующие шаги:")
        print("1. Для Docker: ./docker-auth-new.sh (Linux) или docker-auth-new.bat (Windows)")
        print("2. Для обычного запуска: python auto_auth.py")
        print("3. Для запуска бота: python bot.py")
    else:
        print("\n💥 Обнаружены проблемы!")
        print("📋 Проверьте настройки и повторите тестирование")

if __name__ == "__main__":
    asyncio.run(main())