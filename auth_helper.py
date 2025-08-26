"""
Автоматическая авторизация для Telegram Channel Export Bot
Обрабатывает автоматический вход в Telethon без интерактивного ввода
"""
import asyncio
import logging
import os
from typing import Optional, Callable
from telethon import TelegramClient
from telethon.errors import (
    SessionPasswordNeededError, 
    PhoneCodeExpiredError, 
    PhoneCodeInvalidError,
    FloodWaitError,
    PhoneNumberInvalidError,
    AuthKeyUnregisteredError
)
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
                                        code_callback: Optional[Callable] = None,
                                        interactive: bool = False) -> TelegramClient:
        """
        Создает и авторизует Telegram клиент
        
        Args:
            phone_number: Номер телефона (из переменных окружения если не указан)
            password: Облачный пароль (из переменных окружения если не указан)
            code_callback: Функция для получения кода подтверждения
            interactive: Интерактивный режим для ввода кода
            
        Returns:
            Авторизованный TelegramClient
        """
        
        # Используем данные из конфигурации если не переданы
        phone = phone_number or bot_config.phone_number
        pwd = password or bot_config.password
        
        if not phone:
            raise ValueError("Номер телефона не указан. Установите PHONE_NUMBER в переменных окружения.")
        
        # Проверяем формат номера телефона
        if not phone.startswith('+'):
            logger.warning(f"Номер телефона должен начинаться с '+': {phone}")
        
        logger.info(f"Инициализация клиента для {phone}")
        
        # Создаем клиент
        self.client = TelegramClient(
            self.session_name,
            bot_config.api_id,
            bot_config.api_hash
        )
        
        try:
            logger.info("Подключение к Telegram...")
            await self.client.connect()
            
            # Проверяем, авторизованы ли мы уже
            if await self.client.is_user_authorized():
                logger.info("Пользователь уже авторизован")
                return self.client
                
            return await self._perform_auth(phone, pwd, code_callback, interactive)
            
        except Exception as e:
            logger.error(f"Ошибка создания клиента: {e}")
            if self.client:
                self.client.disconnect()
            raise
    
    async def _perform_auth(self, phone: str, password: Optional[str], 
                           code_callback: Optional[Callable], interactive: bool) -> TelegramClient:
        """Выполняет процесс авторизации"""
        logger.info(f"Начинаю авторизацию для номера {phone}")
        
        if not self.client:
            raise ValueError("Клиент не создан")
        
        try:
            # Отправляем код на телефон
            logger.info("Отправляю запрос на код подтверждения...")
            sent_code = await self.client.send_code_request(phone)
            logger.info(f"Код подтверждения отправлен. Тип: {sent_code.type}")
            
            # Получаем код подтверждения
            code = await self._get_verification_code(code_callback, interactive)
            logger.info("Код подтверждения получен")
            
            # Пытаемся войти с кодом
            try:
                await self.client.sign_in(phone, code)
                logger.info("✅ Успешная авторизация с кодом")
                
            except SessionPasswordNeededError:
                # Требуется облачный пароль
                logger.info("Требуется облачный пароль (2FA)")
                cloud_password = await self._get_cloud_password(password, interactive)
                
                await self.client.sign_in(password=cloud_password)
                logger.info("✅ Успешная авторизация с облачным паролем")
                
        except PhoneNumberInvalidError:
            raise ValueError(f"Неверный номер телефона: {phone}")
            
        except (PhoneCodeExpiredError, PhoneCodeInvalidError) as e:
            logger.error(f"Ошибка с кодом подтверждения: {e}")
            raise ValueError(f"Неверный или истекший код подтверждения: {e}")
            
        except FloodWaitError as e:
            logger.error(f"Слишком много попыток. Подождите {e.seconds} секунд")
            raise ValueError(f"Слишком много попыток. Подождите {e.seconds} секунд")
            
        except AuthKeyUnregisteredError:
            logger.error("Ключ авторизации не зарегистрирован. Удалите файл сессии")
            raise ValueError("Ключ авторизации недействителен. Удалите файл bot_session.session")
        
        logger.info("✅ Авторизация завершена успешно")
        return self.client
    
    async def _get_verification_code(self, code_callback: Optional[Callable], interactive: bool) -> str:
        """Получает код подтверждения"""
        if code_callback:
            return await code_callback()
            
        if interactive:
            # Интерактивный ввод
            code = input("Введите код подтверждения из Telegram: ")
            if not code.strip():
                raise ValueError("Код не может быть пустым")
            return code.strip()
        
        # Получаем из переменной окружения
        code = os.getenv('TELEGRAM_CODE', '').strip()
        if code:
            return code
            
        # Ожидание кода
        logger.info("Ожидание кода подтверждения...")
        max_wait = int(os.getenv('CODE_WAIT_TIMEOUT', '60'))
        wait_interval = 5
        
        for attempt in range(0, max_wait, wait_interval):
            await asyncio.sleep(wait_interval)
            code = os.getenv('TELEGRAM_CODE', '').strip()
            if code:
                logger.info(f"Код получен через {attempt + wait_interval} секунд")
                return code
            logger.debug(f"Ожидание кода... ({attempt + wait_interval}/{max_wait} секунд)")
        
        raise ValueError(f"Код подтверждения не получен в течение {max_wait} секунд")
    
    async def _get_cloud_password(self, password: Optional[str], interactive: bool) -> str:
        """Получает облачный пароль"""
        if password:
            return password
            
        if interactive:
            import getpass
            pwd = getpass.getpass("Введите облачный пароль (2FA): ")
            if not pwd.strip():
                raise ValueError("Пароль не может быть пустым")
            return pwd.strip()
        
        raise ValueError("Облачный пароль не указан. Установите CLOUD_PASSWORD")
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
    
    @staticmethod
    def interactive_auth_prompt():
        """Показывает инструкции для интерактивной авторизации"""
        print("⚡️ Интерактивная авторизация Telegram")
        print("="*50)
        print("📱 Telegram отправит код подтверждения")
        print("🔑 Если включена 2FA, потребуется облачный пароль")
        print("\n")

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