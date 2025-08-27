"""
Telegram Channel Export Bot
Main bot file with handlers and menu system
"""
import logging
import os
import asyncio
from datetime import datetime
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode

from config import bot_config, export_config
from exporters import ChannelExporter
from user_settings import UserSettingsManager
from languages import get_text, get_language_name
from server_monitor import ServerMonitor
from animation_helper import AnimationHelper

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not bot_config.debug_mode else logging.DEBUG
)
logger = logging.getLogger(__name__)

class TelegramExportBot:
    """Main bot class"""
    
    def __init__(self):
        self.application = None
        self.exporter = ChannelExporter()
        self.settings_manager = UserSettingsManager()
        self.server_monitor = ServerMonitor()
        self.animation_helper = AnimationHelper()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        welcome_text = get_text(lang, 'welcome_text', name=user.first_name)
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_settings_menu'), callback_data="main_menu")],
            [InlineKeyboardButton(get_text(lang, 'btn_help'), callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        help_text = get_text(lang, 'help_text')
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_settings_menu'), callback_data="main_menu")],
            [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="start")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        await self.show_main_menu(update, context)

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        language_name = get_language_name(lang, lang)
        media_status = get_text(lang, 'yes') if user_settings.include_media else get_text(lang, 'no')
        last_export = user_settings.last_export or 'Never'
        
        status_text = get_text(lang, 'status_text',
            user_id=user_id,
            language=language_name,
            format=user_settings.export_format.upper(),
            media=media_status,
            max_messages=user_settings.max_messages,
            last_export=last_export,
            current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_settings_menu'), callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            status_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main settings menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        language_name = get_language_name(lang, lang)
        media_status = get_text(lang, 'yes') if user_settings.include_media else get_text(lang, 'no')
        
        menu_text = get_text(lang, 'main_menu_text',
            language=language_name,
            format=user_settings.export_format.upper(),
            media=media_status,
            max_messages=user_settings.max_messages
        )
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_language'), callback_data="language_menu")],
            [InlineKeyboardButton(get_text(lang, 'btn_export_format'), callback_data="format_menu")],
            [InlineKeyboardButton(get_text(lang, 'btn_media_settings'), callback_data="media_menu")],
            [InlineKeyboardButton(get_text(lang, 'btn_message_limit'), callback_data="limit_menu")],
            [InlineKeyboardButton(get_text(lang, 'btn_server_stats'), callback_data="server_stats_menu")],
            [InlineKeyboardButton(get_text(lang, 'btn_reset_settings'), callback_data="reset_settings")],
            [InlineKeyboardButton(get_text(lang, 'btn_help'), callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                menu_text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                menu_text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        data = query.data
        
        if data == "main_menu":
            await self.show_main_menu(update, context)
        elif data == "language_menu":
            await self.show_language_menu(update, context)
        elif data == "format_menu":
            await self.show_format_menu(update, context)
        elif data == "media_menu":
            await self.show_media_menu(update, context)
        elif data == "limit_menu":
            await self.show_limit_menu(update, context)
        elif data == "server_stats_menu":
            await self.show_server_stats_menu(update, context)
        elif data == "system_overview":
            await self.show_system_overview(update, context)
        elif data == "cpu_stats":
            await self.show_cpu_stats(update, context)
        elif data == "memory_stats":
            await self.show_memory_stats(update, context)
        elif data == "disk_stats":
            await self.show_disk_stats(update, context)
        elif data == "network_stats":
            await self.show_network_stats(update, context)
        elif data == "top_processes":
            await self.show_top_processes(update, context)
        elif data.startswith("refresh_"):
            # Handle refresh actions
            refresh_type = data.replace("refresh_", "")
            await self.refresh_stats(update, context, refresh_type)
        elif data == "help":
            await self.show_help(update, context)
        elif data == "reset_settings":
            await self.reset_user_settings(update, context, user_id)
        elif data.startswith("set_language_"):
            language = data.replace("set_language_", "")
            await self.set_language(update, context, user_id, language)
        elif data.startswith("set_format_"):
            format_type = data.replace("set_format_", "")
            await self.set_export_format(update, context, user_id, format_type)
        elif data.startswith("set_media_"):
            include_media = data == "set_media_yes"
            await self.set_media_setting(update, context, user_id, include_media)
        elif data.startswith("set_limit_"):
            limit = int(data.replace("set_limit_", ""))
            await self.set_message_limit(update, context, user_id, limit)

    async def show_language_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show language selection menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        current_language = get_language_name(lang, lang)
        menu_text = get_text(lang, 'language_menu_text', current_language=current_language)
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_english'), callback_data="set_language_en")],
            [InlineKeyboardButton(get_text(lang, 'btn_russian'), callback_data="set_language_ru")],
            [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            menu_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def show_format_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show export format selection menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        menu_text = get_text(lang, 'format_menu_text', format=user_settings.export_format.upper())
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_json'), callback_data="set_format_json")],
            [InlineKeyboardButton(get_text(lang, 'btn_csv'), callback_data="set_format_csv")],
            [InlineKeyboardButton(get_text(lang, 'btn_markdown'), callback_data="set_format_markdown")],
            [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            menu_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def show_media_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show media inclusion menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        media_setting = get_text(lang, 'include_media') if user_settings.include_media else get_text(lang, 'no_media')
        menu_text = get_text(lang, 'media_menu_text', media_setting=media_setting)
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_include_media'), callback_data="set_media_yes")],
            [InlineKeyboardButton(get_text(lang, 'btn_no_media'), callback_data="set_media_no")],
            [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            menu_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def show_limit_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show message limit menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        menu_text = get_text(lang, 'limit_menu_text', limit=user_settings.max_messages)
        
        keyboard = [
            [InlineKeyboardButton("100", callback_data="set_limit_100")],
            [InlineKeyboardButton("500", callback_data="set_limit_500")],
            [InlineKeyboardButton("1000", callback_data="set_limit_1000")],
            [InlineKeyboardButton("5000", callback_data="set_limit_5000")],
            [InlineKeyboardButton("10000", callback_data="set_limit_10000")],
            [InlineKeyboardButton(get_text(lang, 'btn_no_limit'), callback_data="set_limit_0")],
            [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            menu_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        help_text = get_text(lang, 'help_menu_text')
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_back_to_menu'), callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            help_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def set_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, language: str):
        """Set user's language"""
        self.settings_manager.update_user_setting(user_id, 'language', language)
        
        language_name = get_language_name(language, language)
        message_text = get_text(language, 'language_set', language=language_name)
        
        await update.callback_query.edit_message_text(
            message_text,
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def set_export_format(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, format_type: str):
        """Set user's export format"""
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        self.settings_manager.update_user_setting(user_id, 'export_format', format_type)
        
        message_text = get_text(lang, 'format_set', format=format_type.upper())
        
        await update.callback_query.edit_message_text(
            message_text,
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def set_media_setting(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, include_media: bool):
        """Set user's media inclusion setting"""
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        self.settings_manager.update_user_setting(user_id, 'include_media', include_media)
        
        if include_media:
            message_text = get_text(lang, 'media_enabled')
        else:
            message_text = get_text(lang, 'media_disabled')
        
        await update.callback_query.edit_message_text(
            message_text,
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def set_message_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, limit: int):
        """Set user's message limit"""
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        self.settings_manager.update_user_setting(user_id, 'max_messages', limit)
        
        limit_text = get_text(lang, 'no_limit_text') if limit == 0 else f"{limit} messages"
        message_text = get_text(lang, 'limit_set', limit=limit_text)
        
        await update.callback_query.edit_message_text(
            message_text,
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def reset_user_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Reset user settings to defaults"""
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        self.settings_manager.reset_user_settings(user_id)
        
        message_text = get_text(lang, 'settings_reset')
        
        await update.callback_query.edit_message_text(
            message_text,
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def handle_channel_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle channel export requests"""
        user_id = update.effective_user.id
        message_text = update.message.text.strip()
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Extract channel username
        channel_username = self._extract_channel_username(message_text)
        
        if not channel_username:
            await update.message.reply_text(
                get_text(lang, 'invalid_channel')
            )
            return
        
        # Send initial status message
        media_status = get_text(lang, 'included') if user_settings.include_media else get_text(lang, 'excluded')
        status_text = get_text(lang, 'export_starting',
            channel=channel_username,
            format=user_settings.export_format.upper(),
            media=media_status
        )
        
        status_message = await update.message.reply_text(status_text)
        
        try:
            # Start export process
            file_path = await self.exporter.export_channel(
                channel_username=channel_username,
                export_format=user_settings.export_format,
                include_media=user_settings.include_media,
                max_messages=user_settings.max_messages,
                progress_callback=lambda msg: self._update_progress(status_message, msg)
            )
            
            # Send the exported file
            await self._send_export_file(update, context, file_path, channel_username, user_settings)
            
            # Update user's last export time
            self.settings_manager.update_user_setting(user_id, 'last_export', datetime.now().isoformat())
            
        except Exception as e:
            logger.error(f"Export failed for user {user_id}: {str(e)}")
            error_text = get_text(lang, 'export_failed', error=str(e))
            await status_message.edit_text(error_text)

    def _extract_channel_username(self, text: str) -> str:
        """Extract channel username from various formats"""
        text = text.strip()
        
        # Handle t.me links
        if 't.me/' in text:
            text = text.split('t.me/')[-1].split('?')[0]
        
        # Remove @ if present
        if text.startswith('@'):
            text = text[1:]
        
        # Validate username format
        if text and text.replace('_', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').isalpha():
            return text
        
        return ""

    async def _update_progress(self, status_message, progress_text: str):
        """Update progress message"""
        try:
            await status_message.edit_text(progress_text)
        except Exception:
            pass  # Ignore rate limit errors

    async def _send_export_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                               file_path: str, channel_username: str, user_settings):
        """Send the exported file to user"""
        lang = user_settings.language
        
        try:
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            
            caption = get_text(lang, 'export_completed',
                channel=channel_username,
                format=user_settings.export_format.upper(),
                size=file_size,
                time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            with open(file_path, 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )
            
            # Clean up file after sending
            os.remove(file_path)
            
        except Exception as e:
            logger.error(f"Failed to send file: {str(e)}")
            error_text = get_text(lang, 'file_send_failed', error=str(e))
            await update.message.reply_text(error_text)

    # Server Monitoring Methods
    async def show_server_stats_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show server statistics menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        menu_text = get_text(lang, 'server_stats_title')
        
        keyboard = [
            [InlineKeyboardButton(get_text(lang, 'btn_system_overview'), callback_data="system_overview")],
            [InlineKeyboardButton(get_text(lang, 'btn_cpu_stats'), callback_data="cpu_stats")],
            [InlineKeyboardButton(get_text(lang, 'btn_memory_stats'), callback_data="memory_stats")],
            [InlineKeyboardButton(get_text(lang, 'btn_disk_stats'), callback_data="disk_stats")],
            [InlineKeyboardButton(get_text(lang, 'btn_network_stats'), callback_data="network_stats")],
            [InlineKeyboardButton(get_text(lang, 'btn_top_processes'), callback_data="top_processes")],
            [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            menu_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    async def show_system_overview(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show system overview with animated loading"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Show animated loading
        loading_frames = ["🔄 Loading system info", "⚡ Gathering data", "📊 Processing stats"]
        for frame in loading_frames:
            await update.callback_query.edit_message_text(frame)
            await asyncio.sleep(0.8)
        
        try:
            system_info = self.server_monitor.get_system_info()
            uptime_info = self.server_monitor.get_uptime()
            cpu_info = self.server_monitor.get_cpu_usage()
            memory_info = self.server_monitor.get_memory_usage()
            
            # Get system health indicator
            health_emoji = self.animation_helper.get_system_health_emoji(
                cpu_info['usage_percent'], 
                memory_info['percent_used'], 
                75  # Sample disk usage
            )
            
            formatted_uptime = self.animation_helper.format_uptime(uptime_info['system_uptime'])
            
            overview_text = (
                f"🐧 <b>System Overview</b> {health_emoji}\n\n"
                f"🏷️ Hostname: <code>{system_info['hostname']}</code>\n"
                f"💻 OS: {system_info['os']} {system_info['os_version']}\n"
                f"🏗️ Architecture: {system_info['architecture']}\n"
                f"🐍 Python: {system_info['python_version']}\n\n"
                f"⏰ <b>Uptime Information</b>\n"
                f"🖥️ System: {formatted_uptime}\n"
                f"🤖 Bot: {self.animation_helper.format_uptime(uptime_info['bot_uptime'])}\n"
                f"🚀 Boot Time: {uptime_info['boot_time']}\n\n"
                f"📊 <b>Quick Stats</b>\n"
                f"⚡ CPU: {self.animation_helper.get_progress_bar(cpu_info['usage_percent'])}\n"
                f"🧠 RAM: {self.animation_helper.get_progress_bar(memory_info['percent_used'])}\n"
                f"💾 Cores: {cpu_info['core_count']} @ {cpu_info['frequency_mhz']:.0f} MHz"
            )
            
            keyboard = [
                [InlineKeyboardButton(get_text(lang, 'btn_refresh_stats'), callback_data="refresh_system_overview")],
                [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="server_stats_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                overview_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            error_text = get_text(lang, 'stats_error', error=str(e))
            await update.callback_query.edit_message_text(error_text)
    
    async def show_cpu_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show CPU statistics with visual indicators"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Show animated loading
        loading_frames = ["⚡ Scanning CPU", "📊 Measuring performance", "🚀 Analyzing cores"]
        for frame in loading_frames:
            await update.callback_query.edit_message_text(frame)
            await asyncio.sleep(0.7)
        
        try:
            cpu_info = self.server_monitor.get_cpu_usage()
            
            # Generate visual CPU usage
            cpu_visual = self.animation_helper.get_cpu_visual(cpu_info['usage_percent'])
            load_indicator = self.animation_helper.get_load_indicator(
                cpu_info['load_average_1m'], 
                cpu_info['core_count']
            )
            
            cpu_text = (
                f"⚡ <b>CPU Statistics</b>\n\n"
                f"📊 Usage: <b>{cpu_info['usage_percent']:.1f}%</b>\n"
                f"{cpu_visual}\n"
                f"{self.animation_helper.get_progress_bar(cpu_info['usage_percent'])}\n\n"
                f"🔢 Cores: <b>{cpu_info['core_count']}</b>\n"
                f"⚡ Frequency: <b>{cpu_info['frequency_mhz']:.0f} MHz</b>\n\n"
                f"📈 <b>Load Average</b> {load_indicator}\n"
                f"1m: <code>{cpu_info['load_average_1m']:.2f}</code>\n"
                f"5m: <code>{cpu_info['load_average_5m']:.2f}</code>\n"
                f"15m: <code>{cpu_info['load_average_15m']:.2f}</code>"
            )
            
            keyboard = [
                [InlineKeyboardButton(get_text(lang, 'btn_refresh_stats'), callback_data="refresh_cpu_stats")],
                [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="server_stats_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                cpu_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            error_text = get_text(lang, 'stats_error', error=str(e))
            await update.callback_query.edit_message_text(error_text)
    
    async def show_memory_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show memory statistics with visual indicators"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Show animated loading
        loading_frames = ["🧠 Scanning memory", "📊 Analyzing usage", "💾 Checking availability"]
        for frame in loading_frames:
            await update.callback_query.edit_message_text(frame)
            await asyncio.sleep(0.7)
        
        try:
            memory_info = self.server_monitor.get_memory_usage()
            
            # Generate visual memory usage
            memory_visual = self.animation_helper.get_memory_visual(memory_info['percent_used'])
            swap_visual = self.animation_helper.get_memory_visual(memory_info['swap_percent'])
            
            memory_text = (
                f"🧠 <b>Memory Usage</b>\n\n"
                f"📊 RAM Usage: <b>{memory_info['used_gb']:.1f} GB</b> / {memory_info['total_gb']:.1f} GB\n"
                f"{memory_visual}\n"
                f"{self.animation_helper.get_progress_bar(memory_info['percent_used'])}\n\n"
                f"💾 Available: <b>{memory_info['available_gb']:.1f} GB</b>\n\n"
                f"🔄 <b>Swap Memory</b>\n"
                f"💿 Total: <b>{memory_info['swap_total_gb']:.1f} GB</b>\n"
                f"📊 Used: <b>{memory_info['swap_used_gb']:.1f} GB</b>\n"
                f"{swap_visual}\n"
                f"{self.animation_helper.get_progress_bar(memory_info['swap_percent'])}"
            )
            
            keyboard = [
                [InlineKeyboardButton(get_text(lang, 'btn_refresh_stats'), callback_data="refresh_memory_stats")],
                [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="server_stats_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                memory_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            error_text = get_text(lang, 'stats_error', error=str(e))
            await update.callback_query.edit_message_text(error_text)
    
    async def show_disk_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show disk usage statistics with visual indicators"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Show animated loading
        loading_frames = ["💾 Scanning disks", "📁 Analyzing usage", "📊 Calculating space"]
        for frame in loading_frames:
            await update.callback_query.edit_message_text(frame)
            await asyncio.sleep(0.7)
        
        try:
            disk_info = self.server_monitor.get_disk_usage()
            
            disk_text = f"💾 <b>Disk Usage</b>\n\n"
            
            for device, stats in disk_info.items():
                health_emoji = self.animation_helper.get_disk_visual(stats['percent_used'])
                progress_bar = self.animation_helper.get_progress_bar(stats['percent_used'])
                
                disk_item = (
                    f"💽 <b>{device}</b> {health_emoji}\n"
                    f"  📁 Mount: <code>{stats['mountpoint']}</code>\n"
                    f"  📊 Used: <b>{stats['used_gb']:.1f} GB</b> / {stats['total_gb']:.1f} GB\n"
                    f"  {progress_bar}\n"
                    f"  💾 Free: <b>{stats['free_gb']:.1f} GB</b>\n"
                    f"  🗂️ FS: {stats['filesystem']}\n\n"
                )
                disk_text += disk_item
            
            keyboard = [
                [InlineKeyboardButton(get_text(lang, 'btn_refresh_stats'), callback_data="refresh_disk_stats")],
                [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="server_stats_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                disk_text[:4000],  # Limit message length
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            error_text = get_text(lang, 'stats_error', error=str(e))
            await update.callback_query.edit_message_text(error_text)
    
    async def show_network_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show network statistics with activity indicators"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Show animated loading
        loading_frames = ["🌐 Scanning network", "📶 Measuring throughput", "📊 Analyzing traffic"]
        for frame in loading_frames:
            await update.callback_query.edit_message_text(frame)
            await asyncio.sleep(0.7)
        
        try:
            network_info = self.server_monitor.get_network_usage()
            
            network_text = f"🌐 <b>Network Activity</b>\n\n"
            
            active_interfaces = 0
            for interface, stats in list(network_info.items())[:5]:  # Limit to 5 interfaces
                if stats['bytes_sent_total'] > 0 or stats['bytes_recv_total'] > 0:  # Skip inactive interfaces
                    active_interfaces += 1
                    arrows = self.animation_helper.get_network_arrows(
                        stats['bytes_sent_per_sec'], 
                        stats['bytes_recv_per_sec']
                    )
                    
                    sent_formatted = self.animation_helper.format_bytes_with_color(stats['bytes_sent_total'])
                    recv_formatted = self.animation_helper.format_bytes_with_color(stats['bytes_recv_total'])
                    
                    network_item = (
                        f"🔌 <b>{interface}</b> {arrows}\n"
                        f"  📤 Sent: {sent_formatted}\n"
                        f"  📥 Received: {recv_formatted}\n"
                        f"  📊 Rate: ↑{self.server_monitor.format_bytes(stats['bytes_sent_per_sec'])}/s "
                        f"↓{self.server_monitor.format_bytes(stats['bytes_recv_per_sec'])}/s\n"
                        f"  📦 Packets: ↑{stats['packets_sent']:,} ↓{stats['packets_recv']:,}\n"
                    )
                    
                    if stats['errors_out'] > 0 or stats['errors_in'] > 0:
                        network_item += f"  ❌ Errors: ↑{stats['errors_out']} ↓{stats['errors_in']}\n"
                    
                    network_text += network_item + "\n"
            
            if active_interfaces == 0:
                network_text += "😴 No active network interfaces found\n"
            
            keyboard = [
                [InlineKeyboardButton(get_text(lang, 'btn_refresh_stats'), callback_data="refresh_network_stats")],
                [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="server_stats_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                network_text[:4000],  # Limit message length
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            error_text = get_text(lang, 'stats_error', error=str(e))
            await update.callback_query.edit_message_text(error_text)
    
    async def show_top_processes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show top processes with status indicators"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Show animated loading
        loading_frames = ["🔝 Scanning processes", "📊 Ranking by usage", "🏆 Finding top performers"]
        for frame in loading_frames:
            await update.callback_query.edit_message_text(frame)
            await asyncio.sleep(0.8)
        
        try:
            processes = self.server_monitor.get_top_processes(10)
            
            processes_text = f"🔝 <b>Top 10 Processes</b>\n\n"
            
            for i, process in enumerate(processes[:10], 1):
                status_emoji = self.animation_helper.get_status_emoji(process['status'])
                cpu_bar = self.animation_helper.get_progress_bar(process['cpu_percent'], 6)
                memory_bar = self.animation_helper.get_progress_bar(process['memory_percent'], 6)
                
                process_item = (
                    f"{i}. {status_emoji} <b>{process['name'][:15]}</b>\n"
                    f"    🏷️ PID: <code>{process['pid']}</code>\n"
                    f"    ⚡ CPU: {cpu_bar}\n"
                    f"    🧠 RAM: {memory_bar}\n"
                    f"    💾 {process['memory_mb']:.0f} MB | ⏰ {process['uptime']}\n\n"
                )
                processes_text += process_item
            
            keyboard = [
                [InlineKeyboardButton(get_text(lang, 'btn_refresh_stats'), callback_data="refresh_top_processes")],
                [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data="server_stats_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                processes_text[:4000],  # Limit message length
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            error_text = get_text(lang, 'stats_error', error=str(e))
            await update.callback_query.edit_message_text(error_text)
    
    async def refresh_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE, stats_type: str):
        """Refresh specific statistics"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        lang = user_settings.language
        
        # Show refresh confirmation
        refresh_msg = get_text(lang, 'stats_updated')
        await update.callback_query.answer(refresh_msg)
        
        # Redirect to appropriate stats view
        if stats_type == "system_overview":
            await self.show_system_overview(update, context)
        elif stats_type == "cpu_stats":
            await self.show_cpu_stats(update, context)
        elif stats_type == "memory_stats":
            await self.show_memory_stats(update, context)
        elif stats_type == "disk_stats":
            await self.show_disk_stats(update, context)
        elif stats_type == "network_stats":
            await self.show_network_stats(update, context)
        elif stats_type == "top_processes":
            await self.show_top_processes(update, context)

    def run(self):
        """Start the bot"""
        if not bot_config.bot_token:
            logger.error("BOT_TOKEN not configured!")
            return
        
        # Create application
        self.application = Application.builder().token(bot_config.bot_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_channel_message))
        
        # Start bot
        logger.info("Starting Telegram Channel Export Bot...")
        self.application.run_polling()

if __name__ == '__main__':
    # Create exports directory
    os.makedirs(export_config.export_folder, exist_ok=True)
    
    # Start bot
    bot = TelegramExportBot()
    bot.run()