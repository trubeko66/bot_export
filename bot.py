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
        welcome_text = (
            f"👋 Welcome to Channel Export Bot, {user.first_name}!\n\n"
            "I can help you export Telegram channels in various formats:\n"
            "• JSON format\n"
            "• CSV format\n"
            "• Markdown format\n\n"
            "Features:\n"
            "• Export with or without media files\n"
            "• Customizable export settings\n"
            "• Multiple format support\n\n"
            "Send me a channel username/link or use /menu to configure settings."
        )
        
        keyboard = [
            [InlineKeyboardButton("📋 Settings Menu", callback_data="main_menu")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "🔧 <b>How to use the bot:</b>\n\n"
            "1. <b>Setup:</b> Configure your export preferences in the menu\n"
            "2. <b>Export:</b> Send a channel username (e.g., @channelname) or link\n"
            "3. <b>Download:</b> Get your exported file\n\n"
            "<b>Commands:</b>\n"
            "/start - Start the bot\n"
            "/menu - Open settings menu\n"
            "/help - Show this help\n"
            "/status - Check bot status\n\n"
            "<b>Supported formats:</b>\n"
            "• JSON - Complete message data\n"
            "• CSV - Tabular format\n"
            "• Markdown - Human-readable format\n\n"
            "<b>Channel input examples:</b>\n"
            "• @channelname\n"
            "• https://t.me/channelname\n"
            "• channelname (without @)\n"
        )
        
        keyboard = [
            [InlineKeyboardButton("📋 Settings Menu", callback_data="main_menu")],
            [InlineKeyboardButton("🔙 Back", callback_data="start")],
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
        
        status_text = (
            "📊 <b>Bot Status</b>\n\n"
            f"🆔 User ID: {user_id}\n"
            f"📋 Export Format: {user_settings.export_format.upper()}\n"
            f"📎 Include Media: {'Yes' if user_settings.include_media else 'No'}\n"
            f"📏 Max Messages: {user_settings.max_messages}\n"
            f"🕐 Last Export: {user_settings.last_export or 'Never'}\n\n"
            f"🤖 Bot Version: 1.0.0\n"
            f"📅 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        keyboard = [
            [InlineKeyboardButton("📋 Settings Menu", callback_data="main_menu")],
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
        
        menu_text = (
            "⚙️ <b>Export Settings</b>\n\n"
            f"📋 Format: <b>{user_settings.export_format.upper()}</b>\n"
            f"📎 Include Media: <b>{'Yes' if user_settings.include_media else 'No'}</b>\n"
            f"📏 Max Messages: <b>{user_settings.max_messages}</b>\n\n"
            "Select an option to configure:"
        )
        
        keyboard = [
            [InlineKeyboardButton("📋 Export Format", callback_data="format_menu")],
            [InlineKeyboardButton("📎 Media Settings", callback_data="media_menu")],
            [InlineKeyboardButton("📏 Message Limit", callback_data="limit_menu")],
            [InlineKeyboardButton("🔄 Reset to Defaults", callback_data="reset_settings")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
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
        elif data.startswith("set_format_"):
            format_type = data.replace("set_format_", "")
            await self.set_export_format(update, context, user_id, format_type)
        elif data.startswith("set_media_"):
            include_media = data == "set_media_yes"
            await self.set_media_setting(update, context, user_id, include_media)
        elif data.startswith("set_limit_"):
            limit = int(data.replace("set_limit_", ""))
            await self.set_message_limit(update, context, user_id, limit)

    async def show_format_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show export format selection menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        
        menu_text = (
            "📋 <b>Export Format Selection</b>\n\n"
            f"Current format: <b>{user_settings.export_format.upper()}</b>\n\n"
            "<b>Available formats:</b>\n"
            "• JSON - Complete message data with metadata\n"
            "• CSV - Tabular format for spreadsheet apps\n"
            "• Markdown - Human-readable text format\n\n"
            "Select your preferred format:"
        )
        
        keyboard = [
            [InlineKeyboardButton("📄 JSON", callback_data="set_format_json")],
            [InlineKeyboardButton("📊 CSV", callback_data="set_format_csv")],
            [InlineKeyboardButton("📝 Markdown", callback_data="set_format_markdown")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            menu_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def show_media_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show media inclusion menu"""
        user_id = update.effective_user.id
        user_settings = self.settings_manager.get_user_settings(user_id)
        
        menu_text = (
            "📎 <b>Media Settings</b>\n\n"
            f"Current setting: <b>{'Include Media' if user_settings.include_media else 'No Media'}</b>\n\n"
            "<b>Options:</b>\n"
            "• <b>Include Media</b> - Download photos, videos, documents\n"
            "• <b>No Media</b> - Text messages only (faster export)\n\n"
            "⚠️ Note: Including media increases export time and file size."
        )
        
        keyboard = [
            [InlineKeyboardButton("✅ Include Media", callback_data="set_media_yes")],
            [InlineKeyboardButton("❌ No Media", callback_data="set_media_no")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
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
        
        menu_text = (
            "📏 <b>Message Limit Settings</b>\n\n"
            f"Current limit: <b>{user_settings.max_messages} messages</b>\n\n"
            "Choose the maximum number of messages to export:"
        )
        
        keyboard = [
            [InlineKeyboardButton("100", callback_data="set_limit_100")],
            [InlineKeyboardButton("500", callback_data="set_limit_500")],
            [InlineKeyboardButton("1000", callback_data="set_limit_1000")],
            [InlineKeyboardButton("5000", callback_data="set_limit_5000")],
            [InlineKeyboardButton("10000", callback_data="set_limit_10000")],
            [InlineKeyboardButton("No Limit", callback_data="set_limit_0")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            menu_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        help_text = (
            "ℹ️ <b>Help & Information</b>\n\n"
            "<b>How to export a channel:</b>\n"
            "1. Configure your settings in the menu\n"
            "2. Send a channel username or link\n"
            "3. Wait for the export to complete\n"
            "4. Download your file\n\n"
            "<b>Supported channel formats:</b>\n"
            "• @channelname\n"
            "• https://t.me/channelname\n"
            "• channelname\n\n"
            "<b>Need more help?</b>\n"
            "Contact the bot administrator."
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            help_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def set_export_format(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, format_type: str):
        """Set user's export format"""
        self.settings_manager.update_user_setting(user_id, 'export_format', format_type)
        
        await update.callback_query.edit_message_text(
            f"✅ Export format set to <b>{format_type.upper()}</b>",
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def set_media_setting(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, include_media: bool):
        """Set user's media inclusion setting"""
        self.settings_manager.update_user_setting(user_id, 'include_media', include_media)
        
        status = "enabled" if include_media else "disabled"
        await update.callback_query.edit_message_text(
            f"✅ Media inclusion <b>{status}</b>",
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def set_message_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, limit: int):
        """Set user's message limit"""
        self.settings_manager.update_user_setting(user_id, 'max_messages', limit)
        
        limit_text = "No limit" if limit == 0 else f"{limit} messages"
        await update.callback_query.edit_message_text(
            f"✅ Message limit set to <b>{limit_text}</b>",
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def reset_user_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Reset user settings to defaults"""
        self.settings_manager.reset_user_settings(user_id)
        
        await update.callback_query.edit_message_text(
            "✅ Settings reset to defaults",
            parse_mode=ParseMode.HTML
        )
        
        # Show main menu after a short delay
        await asyncio.sleep(1)
        await self.show_main_menu(update, context)

    async def handle_channel_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle channel export requests"""
        user_id = update.effective_user.id
        message_text = update.message.text.strip()
        
        # Extract channel username
        channel_username = self._extract_channel_username(message_text)
        
        if not channel_username:
            await update.message.reply_text(
                "❌ Invalid channel format. Please send:\n"
                "• @channelname\n"
                "• https://t.me/channelname\n"
                "• channelname"
            )
            return
        
        user_settings = self.settings_manager.get_user_settings(user_id)
        
        # Send initial status message
        status_message = await update.message.reply_text(
            f"🔄 Starting export of @{channel_username}...\n"
            f"Format: {user_settings.export_format.upper()}\n"
            f"Media: {'Included' if user_settings.include_media else 'Excluded'}"
        )
        
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
            await status_message.edit_text(
                f"❌ Export failed: {str(e)}\n\n"
                "Please check the channel username and try again."
            )

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
        try:
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            
            caption = (
                f"📁 Export completed for @{channel_username}\n"
                f"📋 Format: {user_settings.export_format.upper()}\n"
                f"📏 File size: {file_size:.2f} MB\n"
                f"🕐 Exported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
            await update.message.reply_text(
                f"❌ Failed to send export file: {str(e)}"
            )

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