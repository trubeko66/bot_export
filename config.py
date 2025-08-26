"""
Configuration management for Telegram Channel Export Bot
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    """Bot configuration class"""
    bot_token: str
    api_id: int
    api_hash: str
    admin_user_id: Optional[int] = None
    debug_mode: bool = False
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        return cls(
            bot_token=os.getenv('BOT_TOKEN', ''),
            api_id=int(os.getenv('API_ID', '0')),
            api_hash=os.getenv('API_HASH', ''),
            admin_user_id=int(os.getenv('ADMIN_USER_ID', '0')) if os.getenv('ADMIN_USER_ID') else None,
            debug_mode=os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        )

@dataclass
class ExportConfig:
    """Export configuration class"""
    default_format: str = 'json'
    include_media_by_default: bool = False
    max_messages_per_export: int = 10000
    export_folder: str = 'exports'
    
    @classmethod
    def from_env(cls):
        """Load export configuration from environment variables"""
        return cls(
            default_format=os.getenv('DEFAULT_EXPORT_FORMAT', 'json'),
            include_media_by_default=os.getenv('INCLUDE_MEDIA_BY_DEFAULT', 'false').lower() == 'true',
            max_messages_per_export=int(os.getenv('MAX_MESSAGES_PER_EXPORT', '10000')),
            export_folder=os.getenv('EXPORT_FOLDER', 'exports')
        )

# Initialize configurations
bot_config = BotConfig.from_env()
export_config = ExportConfig.from_env()