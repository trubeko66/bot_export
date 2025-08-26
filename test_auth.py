#!/usr/bin/env python3
"""
Тестирование системы автоматической авторизации
Проверяет все компоненты автоавторизации
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
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Проверяет переменные окружения"""
    logger.info("🔍 Проверка переменных окружения...")
    
    required_vars = ['BOT_TOKEN', 'API_ID', 'API_HASH', 'PHONE_NUMBER']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            if var == 'PHONE_NUMBER':
                logger.info(f"  📱 {var}: {value}")
            elif var in ['BOT_TOKEN', 'API_HASH']:
                logger.info(f"  🔑 {var}: {'*' * 10}")
            else:
                logger.info(f"  ✅ {var}: {value}")
    
    optional_vars = ['CLOUD_PASSWORD', 'TELEGRAM_CODE']
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"  🔐 {var}: {'*' * len(value)}")
        else:
            logger.info(f"  ⚪ {var}: не установлен")
    
    if missing_vars:
        logger.error(f"❌ Отсутствуют обязательные переменные: {', '.join(missing_vars)}")
        return False
    
    logger.info("✅ Все обязательные переменные установлены")
    return True

def check_files():
    """Проверяет наличие необходимых файлов"""
    logger.info("🔍 Проверка файлов...")
    
    required_files = [
        'config.py',
        'auth_helper.py',
        'bot.py',
        'exporters.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            logger.info(f"  ✅ {file}")
    
    if missing_files:
        logger.error(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    logger.info("✅ Все необходимые файлы найдены")
    return True

async def test_config():
    """Тестирует загрузку конфигурации"""
    logger.info("🔍 Тестирование конфигурации...")
    
    try:
        from config import bot_config
        logger.info(f"  📱 Номер телефона: {bot_config.phone_number}")
        logger.info(f"  🆔 API ID: {bot_config.api_id}")
        logger.info(f"  🔑 API Hash: {'*' * 10}")
        logger.info(f"  🤖 Bot Token: {'*' * 10}")
        
        if bot_config.password:
            logger.info(f"  🔐 Облачный пароль: установлен")
        else:
            logger.info(f"  🔐 Облачный пароль: не установлен")
        
        logger.info("✅ Конфигурация загружена успешно")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки конфигурации: {e}")
        return False

async def test_auth_helper():
    """Тестирует модуль автоавторизации"""
    logger.info("🔍 Тестирование модуля авторизации...")
    
    try:
        from auth_helper import AutoAuth, auto_auth
        logger.info("  ✅ Модуль auth_helper импортирован")
        
        # Создаем экземпляр
        auth = AutoAuth("test_session")
        logger.info("  ✅ Экземпляр AutoAuth создан")
        
        logger.info("✅ Модуль авторизации работает")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка модуля авторизации: {e}")
        return False

async def main():
    """Основная функция тестирования"""
    logger.info("🧪 Тестирование системы автоматической авторизации")
    logger.info("=" * 60)
    
    tests = [
        ("Переменные окружения", check_environment),
        ("Файлы проекта", check_files),
        ("Конфигурация", test_config),
        ("Модуль авторизации", test_auth_helper),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Тест: {test_name}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                logger.info(f"✅ {test_name}: ПРОШЕЛ")
                passed += 1
            else:
                logger.error(f"❌ {test_name}: НЕ ПРОШЕЛ")
                
        except Exception as e:
            logger.error(f"💥 {test_name}: ОШИБКА - {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 Результаты тестирования: {passed}/{total} тестов прошли")
    
    if passed == total:
        logger.info("🎉 Все тесты прошли успешно!")
        logger.info("📋 Система готова к использованию")
        
        logger.info("\n📋 Следующие шаги:")
        logger.info("1. Для первоначальной авторизации: python auto_auth.py")
        logger.info("2. Для Docker: ./docker-auth.sh (Linux) или docker-auth.bat (Windows)")
        logger.info("3. Для запуска бота: python bot.py")
        
    else:
        logger.error("💥 Не все тесты прошли!")
        logger.error("📋 Исправьте ошибки перед использованием")

if __name__ == "__main__":
    asyncio.run(main())