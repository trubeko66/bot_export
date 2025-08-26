#!/usr/bin/env python3
"""
Автоматизированная авторизация Telegram для Docker
Использует данные из переменных окружения для полностью автоматической авторизации
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Добавляем путь к модулям бота
sys.path.append(str(Path(__file__).parent))

from auth_helper import auto_auth
from config import bot_config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_auth():
    """Тестирует автоматическую авторизацию"""
    try:
        logger.info("🚀 Начинаю автоматическую авторизацию...")
        
        # Проверяем обязательные переменные
        required_vars = ['BOT_TOKEN', 'API_ID', 'API_HASH', 'PHONE_NUMBER']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"❌ Отсутствуют обязательные переменные: {', '.join(missing_vars)}")
            return False
        
        logger.info(f"📱 Используется номер: {bot_config.phone_number}")
        
        # Пытаемся создать авторизованный клиент
        client = await auto_auth.create_authenticated_client()
        
        # Проверяем что авторизация прошла успешно
        if await client.is_user_authorized():
            try:
                me = await client.get_me()
                name = getattr(me, 'first_name', 'Unknown')
                username = getattr(me, 'username', 'no_username')
                logger.info(f"✅ Авторизация успешна! Пользователь: {name} (@{username})")
            except Exception as e:
                logger.info(f"✅ Авторизация успешна! (Ошибка получения данных пользователя: {e})")
            
            # Закрываем соединение
            client.disconnect()
            
            logger.info("💾 Сессия сохранена в bot_session.session")
            return True
        else:
            logger.error("❌ Авторизация не удалась")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка авторизации: {e}")
        return False

async def main():
    """Основная функция"""
    logger.info("🤖 Автоматизированная авторизация Telegram Bot")
    logger.info("=" * 50)
    
    success = await test_auth()
    
    if success:
        logger.info("🎉 Авторизация завершена успешно!")
        logger.info("📋 Теперь можно запускать основного бота")
        sys.exit(0)
    else:
        logger.error("💥 Авторизация не удалась")
        logger.error("📋 Проверьте переменные окружения и повторите попытку")
        sys.exit(1)

if __name__ == "__main__":
    # Запускаем авторизацию
    asyncio.run(main())