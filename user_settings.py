"""
User Settings Manager for Telegram Channel Export Bot
Handles user preferences and settings persistence
"""
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime

from config import export_config

@dataclass
class UserSettings:
    """User settings data class"""
    user_id: int
    export_format: str = 'json'
    include_media: bool = False
    max_messages: int = 10000
    last_export: Optional[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

class UserSettingsManager:
    """Manages user settings with file-based persistence"""
    
    def __init__(self, settings_file: str = "user_settings.json"):
        self.settings_file = settings_file
        self.settings_cache: Dict[int, UserSettings] = {}
        self._load_settings()
    
    def _load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for user_id_str, settings_dict in data.items():
                    user_id = int(user_id_str)
                    self.settings_cache[user_id] = UserSettings(**settings_dict)
                    
            except Exception as e:
                print(f"Error loading settings: {e}")
                self.settings_cache = {}
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            data = {}
            for user_id, settings in self.settings_cache.items():
                data[str(user_id)] = asdict(settings)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get_user_settings(self, user_id: int) -> UserSettings:
        """Get user settings, create default if not exists"""
        if user_id not in self.settings_cache:
            self.settings_cache[user_id] = UserSettings(
                user_id=user_id,
                export_format=export_config.default_format,
                include_media=export_config.include_media_by_default,
                max_messages=export_config.max_messages_per_export
            )
            self._save_settings()
        
        return self.settings_cache[user_id]
    
    def update_user_setting(self, user_id: int, setting_name: str, value: Any):
        """Update a specific user setting"""
        settings = self.get_user_settings(user_id)
        
        if hasattr(settings, setting_name):
            setattr(settings, setting_name, value)
            settings.updated_at = datetime.now().isoformat()
            self._save_settings()
        else:
            raise ValueError(f"Invalid setting name: {setting_name}")
    
    def update_user_settings(self, user_id: int, settings_dict: Dict[str, Any]):
        """Update multiple user settings"""
        settings = self.get_user_settings(user_id)
        
        for setting_name, value in settings_dict.items():
            if hasattr(settings, setting_name):
                setattr(settings, setting_name, value)
            else:
                raise ValueError(f"Invalid setting name: {setting_name}")
        
        settings.updated_at = datetime.now().isoformat()
        self._save_settings()
    
    def reset_user_settings(self, user_id: int):
        """Reset user settings to defaults"""
        self.settings_cache[user_id] = UserSettings(
            user_id=user_id,
            export_format=export_config.default_format,
            include_media=export_config.include_media_by_default,
            max_messages=export_config.max_messages_per_export
        )
        self._save_settings()
    
    def delete_user_settings(self, user_id: int):
        """Delete user settings"""
        if user_id in self.settings_cache:
            del self.settings_cache[user_id]
            self._save_settings()
    
    def get_all_users(self) -> Dict[int, UserSettings]:
        """Get all user settings"""
        return self.settings_cache.copy()
    
    def get_users_count(self) -> int:
        """Get total number of users"""
        return len(self.settings_cache)
    
    def get_users_by_setting(self, setting_name: str, value: Any) -> Dict[int, UserSettings]:
        """Get users with specific setting value"""
        result = {}
        for user_id, settings in self.settings_cache.items():
            if hasattr(settings, setting_name) and getattr(settings, setting_name) == value:
                result[user_id] = settings
        return result