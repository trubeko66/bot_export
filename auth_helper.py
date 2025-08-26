"""
Автоматическая авторизация для Telegram Channel Export Bot
Обрабатывает автоматический вход в Telethon без интерактивного ввода
"""
import asyncio
import logging
from typing import Optional, Callable
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeExpiredError, PhoneCodeInvalidError
from config import bot_config

logger = logging.getLogger(__name__)

class AutoAuth:
    """Класс для автоматической авторизации в Telegram"""
    
    def __init__(self, session_name: str = "bot_session"):
        self.session_name = session_name
        self.client = None
        
    async def create_authenticated_client(self, 
                                        phone_number: Optional[str] = None,
                                        password: Optional[str] = None,
                                        code_callback: Optional[Callable] = None) -> TelegramClient:
        """
        Создает и авторизует Telegram клиент
        
        Args:
            phone_number: Номер телефона (из переменных окружения если не указан)
            password: Облачный пароль (из переменных окружения если не указан)
            code_callback: Функция для получения кода подтверждения
            
        Returns:
            Авторизованный TelegramClient
        """
        
        # Используем данные из конфигурации если не переданы
        phone = phone_number or bot_config.phone_number
        pwd = password or bot_config.password
        
        if not phone:
            raise ValueError("Номер телефона не указан. Установите PHONE_NUMBER в переменных окружения.")
        
        # Создаем клиент
        self.client = TelegramClient(
            self.session_name,
            bot_config.api_id,
            bot_config.api_hash
        )
        
        logger.info("Подключение к Telegram...")
        await self.client.connect()
        
        # Проверяем, авторизованы ли мы уже
        if await self.client.is_user_authorized():
            logger.info("Пользователь уже авторизован")
            return self.client
        
        logger.info(f"Начинаю авторизацию для номера {phone}")
        
        try:
            # Отправляем код на телефон
            await self.client.send_code_request(phone)
            logger.info("Код подтверждения отправлен")
            
            # Получаем код подтверждения
            if code_callback:
                code = await code_callback()
            else:
                # Пытаемся получить код из переменной окружения
                import os
                code = os.getenv('TELEGRAM_CODE', '')
                if not code:
                    raise ValueError("Код подтверждения не найден. Установите TELEGRAM_CODE или используйте code_callback.")
            
            # Пытаемся войти с кодом
            try:
                await self.client.sign_in(phone, code)
                logger.info("Успешная авторизация с кодом")
                
            except SessionPasswordNeededError:
                # Требуется облачный пароль
                logger.info("Требуется облачный пароль")
                if not pwd:
                    raise ValueError("Облачный пароль не указан. Установите CLOUD_PASSWORD в переменных окружения.")
                
                await self.client.sign_in(password=pwd)
                logger.info("Успешная авторизация с облачным паролем")
                
        except (PhoneCodeExpiredError, PhoneCodeInvalidError) as e:
            logger.error(f"Ошибка с кодом подтверждения: {e}")
            raise ValueError(f"Неверный или истекший код подтверждения: {e}")
        
        except Exception as e:
            logger.error(f"Ошибка авторизации: {e}")
            if self.client:
                self.client.disconnect()
            raise
        
        logger.info("Авторизация завершена успешно")
        return self.client
    
    async def get_or_create_client(self) -> TelegramClient:
        """
        Получает существующий клиент или создает новый с автоавторизацией
        
        Returns:
            Авторизованный TelegramClient
        """
        if self.client and self.client.is_connected():
            if await self.client.is_user_authorized():
                return self.client
        
        return await self.create_authenticated_client()
    
    async def close(self):
        """Закрывает соединение с Telegram"""
        if self.client:
            self.client.disconnect()
            self.client = None

class CodeFromEnv:
    """Класс для получения кода подтверждения из переменных окружения"""
    
    @staticmethod
    async def get_code() -> str:
        """
        Получает код подтверждения из переменной окружения
        
        Returns:
            Код подтверждения
        """
        import os
        code = os.getenv('TELEGRAM_CODE', '')
        if not code:
            # Пытаемся подождать код в течение определенного времени
            max_wait = int(os.getenv('CODE_WAIT_TIMEOUT', '60'))  # 60 секунд по умолчанию
            wait_interval = 5  # проверяем каждые 5 секунд
            
            for _ in range(0, max_wait, wait_interval):
                await asyncio.sleep(wait_interval)
                code = os.getenv('TELEGRAM_CODE', '')
                if code:
                    break
                    
            if not code:
                raise ValueError(f"Код подтверждения не найден в течение {max_wait} секунд")
        
        return code

# Глобальный экземпляр для использования в приложении
auto_auth = AutoAuth()