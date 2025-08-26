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