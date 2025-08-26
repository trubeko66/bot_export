"""
Language Support for Telegram Channel Export Bot
Handles interface translations between English and Russian
"""

LANGUAGES = {
    'en': {
        'welcome_text': (
            "👋 Welcome to Channel Export Bot, {name}!\n\n"
            "I can help you export Telegram channels in various formats:\n"
            "• JSON format\n"
            "• CSV format\n"
            "• Markdown format\n\n"
            "Features:\n"
            "• Export with or without media files\n"
            "• Customizable export settings\n"
            "• Multiple format support\n\n"
            "Send me a channel username/link or use /menu to configure settings."
        ),
        'help_text': (
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
        ),
        'status_text': (
            "📊 <b>Bot Status</b>\n\n"
            "🆔 User ID: {user_id}\n"
            "🌐 Language: {language}\n"
            "📋 Export Format: {format}\n"
            "📎 Include Media: {media}\n"
            "📏 Max Messages: {max_messages}\n"
            "🕐 Last Export: {last_export}\n\n"
            "🤖 Bot Version: 1.0.0\n"
            "📅 Current Time: {current_time}"
        ),
        'main_menu_text': (
            "⚙️ <b>Export Settings</b>\n\n"
            "🌐 Language: <b>{language}</b>\n"
            "📋 Format: <b>{format}</b>\n"
            "📎 Include Media: <b>{media}</b>\n"
            "📏 Max Messages: <b>{max_messages}</b>\n\n"
            "Select an option to configure:"
        ),
        'format_menu_text': (
            "📋 <b>Export Format Selection</b>\n\n"
            "Current format: <b>{format}</b>\n\n"
            "<b>Available formats:</b>\n"
            "• JSON - Complete message data with metadata\n"
            "• CSV - Tabular format for spreadsheet apps\n"
            "• Markdown - Human-readable text format\n\n"
            "Select your preferred format:"
        ),
        'media_menu_text': (
            "📎 <b>Media Settings</b>\n\n"
            "Current setting: <b>{media_setting}</b>\n\n"
            "<b>Options:</b>\n"
            "• <b>Include Media</b> - Download photos, videos, documents\n"
            "• <b>No Media</b> - Text messages only (faster export)\n\n"
            "⚠️ Note: Including media increases export time and file size."
        ),
        'limit_menu_text': (
            "📏 <b>Message Limit Settings</b>\n\n"
            "Current limit: <b>{limit} messages</b>\n\n"
            "Choose the maximum number of messages to export:"
        ),
        'help_menu_text': (
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
        ),
        'language_menu_text': (
            "🌐 <b>Language Settings</b>\n\n"
            "Current language: <b>{current_language}</b>\n\n"
            "Select your preferred language:"
        ),
        # Buttons
        'btn_settings_menu': "📋 Settings Menu",
        'btn_help': "ℹ️ Help",
        'btn_language': "🌐 Language",
        'btn_export_format': "📋 Export Format",
        'btn_media_settings': "📎 Media Settings",
        'btn_message_limit': "📏 Message Limit",
        'btn_reset_settings': "🔄 Reset to Defaults",
        'btn_back': "🔙 Back",
        'btn_back_to_menu': "🔙 Back to Menu",
        'btn_json': "📄 JSON",
        'btn_csv': "📊 CSV",
        'btn_markdown': "📝 Markdown",
        'btn_include_media': "✅ Include Media",
        'btn_no_media': "❌ No Media",
        'btn_no_limit': "No Limit",
        'btn_english': "🇺🇸 English",
        'btn_russian': "🇷🇺 Русский",
        # Status messages
        'yes': "Yes",
        'no': "No",
        'english': "English",
        'russian': "Russian",
        'include_media': "Include Media",
        'no_media': "No Media",
        'format_set': "✅ Export format set to <b>{format}</b>",
        'media_enabled': "✅ Media inclusion <b>enabled</b>",
        'media_disabled': "✅ Media inclusion <b>disabled</b>",
        'limit_set': "✅ Message limit set to <b>{limit}</b>",
        'language_set': "✅ Language set to <b>{language}</b>",
        'settings_reset': "✅ Settings reset to defaults",
        'invalid_channel': (
            "❌ Invalid channel format. Please send:\n"
            "• @channelname\n"
            "• https://t.me/channelname\n"
            "• channelname"
        ),
        'export_starting': "🔄 Starting export of @{channel}...\nFormat: {format}\nMedia: {media}",
        'export_completed': (
            "📁 Export completed for @{channel}\n"
            "📋 Format: {format}\n"
            "📏 File size: {size:.2f} MB\n"
            "🕐 Exported at: {time}"
        ),
        'export_failed': "❌ Export failed: {error}\n\nPlease check the channel username and try again.",
        'file_send_failed': "❌ Failed to send export file: {error}",
        'included': "Included",
        'excluded': "Excluded",
        'no_limit_text': "No limit"
    },
    'ru': {
        'welcome_text': (
            "👋 Добро пожаловать в бот экспорта каналов, {name}!\n\n"
            "Я могу помочь вам экспортировать Telegram каналы в различных форматах:\n"
            "• Формат JSON\n"
            "• Формат CSV\n"
            "• Формат Markdown\n\n"
            "Возможности:\n"
            "• Экспорт с медиафайлами или без них\n"
            "• Настраиваемые параметры экспорта\n"
            "• Поддержка множества форматов\n\n"
            "Отправьте мне имя пользователя/ссылку канала или используйте /menu для настройки."
        ),
        'help_text': (
            "🔧 <b>Как использовать бота:</b>\n\n"
            "1. <b>Настройка:</b> Настройте параметры экспорта в меню\n"
            "2. <b>Экспорт:</b> Отправьте имя канала (например, @channelname) или ссылку\n"
            "3. <b>Загрузка:</b> Получите экспортированный файл\n\n"
            "<b>Команды:</b>\n"
            "/start - Запустить бота\n"
            "/menu - Открыть меню настроек\n"
            "/help - Показать эту справку\n"
            "/status - Проверить статус бота\n\n"
            "<b>Поддерживаемые форматы:</b>\n"
            "• JSON - Полные данные сообщений\n"
            "• CSV - Табличный формат\n"
            "• Markdown - Человекочитаемый формат\n\n"
            "<b>Примеры ввода канала:</b>\n"
            "• @channelname\n"
            "• https://t.me/channelname\n"
            "• channelname (без @)\n"
        ),
        'status_text': (
            "📊 <b>Статус бота</b>\n\n"
            "🆔 ID пользователя: {user_id}\n"
            "🌐 Язык: {language}\n"
            "📋 Формат экспорта: {format}\n"
            "📎 Включить медиа: {media}\n"
            "📏 Максимум сообщений: {max_messages}\n"
            "🕐 Последний экспорт: {last_export}\n\n"
            "🤖 Версия бота: 1.0.0\n"
            "📅 Текущее время: {current_time}"
        ),
        'main_menu_text': (
            "⚙️ <b>Настройки экспорта</b>\n\n"
            "🌐 Язык: <b>{language}</b>\n"
            "📋 Формат: <b>{format}</b>\n"
            "📎 Включить медиа: <b>{media}</b>\n"
            "📏 Максимум сообщений: <b>{max_messages}</b>\n\n"
            "Выберите опцию для настройки:"
        ),
        'format_menu_text': (
            "📋 <b>Выбор формата экспорта</b>\n\n"
            "Текущий формат: <b>{format}</b>\n\n"
            "<b>Доступные форматы:</b>\n"
            "• JSON - Полные данные сообщений с метаданными\n"
            "• CSV - Табличный формат для электронных таблиц\n"
            "• Markdown - Человекочитаемый текстовый формат\n\n"
            "Выберите предпочтительный формат:"
        ),
        'media_menu_text': (
            "📎 <b>Настройки медиафайлов</b>\n\n"
            "Текущая настройка: <b>{media_setting}</b>\n\n"
            "<b>Опции:</b>\n"
            "• <b>Включить медиа</b> - Загружать фото, видео, документы\n"
            "• <b>Без медиа</b> - Только текстовые сообщения (быстрый экспорт)\n\n"
            "⚠️ Примечание: Включение медиа увеличивает время экспорта и размер файла."
        ),
        'limit_menu_text': (
            "📏 <b>Настройки лимита сообщений</b>\n\n"
            "Текущий лимит: <b>{limit} сообщений</b>\n\n"
            "Выберите максимальное количество сообщений для экспорта:"
        ),
        'help_menu_text': (
            "ℹ️ <b>Справка и информация</b>\n\n"
            "<b>Как экспортировать канал:</b>\n"
            "1. Настройте свои параметры в меню\n"
            "2. Отправьте имя пользователя или ссылку канала\n"
            "3. Дождитесь завершения экспорта\n"
            "4. Загрузите ваш файл\n\n"
            "<b>Поддерживаемые форматы каналов:</b>\n"
            "• @channelname\n"
            "• https://t.me/channelname\n"
            "• channelname\n\n"
            "<b>Нужна дополнительная помощь?</b>\n"
            "Обратитесь к администратору бота."
        ),
        'language_menu_text': (
            "🌐 <b>Настройки языка</b>\n\n"
            "Текущий язык: <b>{current_language}</b>\n\n"
            "Выберите предпочтительный язык:"
        ),
        # Buttons
        'btn_settings_menu': "📋 Меню настроек",
        'btn_help': "ℹ️ Справка",
        'btn_language': "🌐 Язык",
        'btn_export_format': "📋 Формат экспорта",
        'btn_media_settings': "📎 Настройки медиа",
        'btn_message_limit': "📏 Лимит сообщений",
        'btn_reset_settings': "🔄 Сбросить настройки",
        'btn_back': "🔙 Назад",
        'btn_back_to_menu': "🔙 Назад в меню",
        'btn_json': "📄 JSON",
        'btn_csv': "📊 CSV",
        'btn_markdown': "📝 Markdown",
        'btn_include_media': "✅ Включить медиа",
        'btn_no_media': "❌ Без медиа",
        'btn_no_limit': "Без лимита",
        'btn_english': "🇺🇸 English",
        'btn_russian': "🇷🇺 Русский",
        # Status messages
        'yes': "Да",
        'no': "Нет",
        'english': "Английский",
        'russian': "Русский",
        'include_media': "Включить медиа",
        'no_media': "Без медиа",
        'format_set': "✅ Формат экспорта установлен на <b>{format}</b>",
        'media_enabled': "✅ Включение медиа <b>включено</b>",
        'media_disabled': "✅ Включение медиа <b>отключено</b>",
        'limit_set': "✅ Лимит сообщений установлен на <b>{limit}</b>",
        'language_set': "✅ Язык установлен на <b>{language}</b>",
        'settings_reset': "✅ Настройки сброшены к значениям по умолчанию",
        'invalid_channel': (
            "❌ Неверный формат канала. Пожалуйста, отправьте:\n"
            "• @channelname\n"
            "• https://t.me/channelname\n"
            "• channelname"
        ),
        'export_starting': "🔄 Начинаю экспорт @{channel}...\nФормат: {format}\nМедиа: {media}",
        'export_completed': (
            "📁 Экспорт завершен для @{channel}\n"
            "📋 Формат: {format}\n"
            "📏 Размер файла: {size:.2f} МБ\n"
            "🕐 Экспортировано в: {time}"
        ),
        'export_failed': "❌ Экспорт не удался: {error}\n\nПроверьте имя канала и попробуйте снова.",
        'file_send_failed': "❌ Не удалось отправить файл экспорта: {error}",
        'included': "Включено",
        'excluded': "Исключено",
        'no_limit_text': "Без лимита"
    }
}

def get_text(lang: str, key: str, **kwargs) -> str:
    """Get localized text with optional formatting"""
    text = LANGUAGES.get(lang, LANGUAGES['en']).get(key, LANGUAGES['en'].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text

def get_language_name(lang: str, display_lang: str = None) -> str:
    """Get language name in specified display language"""
    if display_lang is None:
        display_lang = lang
    
    if lang == 'en':
        return get_text(display_lang, 'english')
    elif lang == 'ru':
        return get_text(display_lang, 'russian')
    return lang