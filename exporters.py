"""
Channel Export Functionality for Telegram Channel Export Bot
Handles channel data extraction and export in multiple formats
"""
import os
import json
import csv
import asyncio
import aiofiles
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import pytz

from config import bot_config, export_config

class ChannelExporter:
    """Handles channel export operations"""
    
    def __init__(self):
        self.client = None
        self.session_name = "bot_session"
    
    async def _get_client(self) -> TelegramClient:
        """Get or create Telegram client"""
        if self.client is None:
            self.client = TelegramClient(
                self.session_name,
                bot_config.api_id,
                bot_config.api_hash
            )
            await self.client.start()
        return self.client
    
    async def export_channel(self, 
                           channel_username: str,
                           export_format: str = 'json',
                           include_media: bool = False,
                           max_messages: int = 10000,
                           progress_callback: Optional[Callable] = None) -> str:
        """
        Export channel messages in specified format
        
        Args:
            channel_username: Channel username without @
            export_format: 'json', 'csv', or 'markdown'
            include_media: Whether to download media files
            max_messages: Maximum number of messages to export (0 = no limit)
            progress_callback: Function to call with progress updates
            
        Returns:
            Path to the exported file
        """
        
        if progress_callback:
            await progress_callback("🔗 Connecting to Telegram...")
        
        client = await self._get_client()
        
        try:
            # Get channel entity
            channel = await client.get_entity(channel_username)
            
            if progress_callback:
                await progress_callback(f"📡 Found channel: {channel.title}\n🔄 Fetching messages...")
            
            # Fetch messages
            messages = await self._fetch_messages(client, channel, max_messages, progress_callback)
            
            if progress_callback:
                await progress_callback(f"📝 Processing {len(messages)} messages...")
            
            # Process messages
            processed_messages = []
            media_files = []
            
            for i, message in enumerate(messages):
                processed_msg = await self._process_message(message, include_media, client)
                processed_messages.append(processed_msg)
                
                if include_media and processed_msg.get('media_file'):
                    media_files.append(processed_msg['media_file'])
                
                if progress_callback and i % 100 == 0:
                    await progress_callback(f"📝 Processed {i+1}/{len(messages)} messages...")
            
            if progress_callback:
                await progress_callback(f"💾 Exporting to {export_format.upper()} format...")
            
            # Export to specified format
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{channel_username}_{timestamp}.{export_format}"
            filepath = os.path.join(export_config.export_folder, filename)
            
            if export_format == 'json':
                await self._export_to_json(processed_messages, filepath, channel)
            elif export_format == 'csv':
                await self._export_to_csv(processed_messages, filepath, channel)
            elif export_format == 'markdown':
                await self._export_to_markdown(processed_messages, filepath, channel, media_files)
            else:
                raise ValueError(f"Unsupported export format: {export_format}")
            
            if progress_callback:
                await progress_callback(f"✅ Export completed: {filename}")
            
            return filepath
            
        except Exception as e:
            if progress_callback:
                await progress_callback(f"❌ Export failed: {str(e)}")
            raise e
    
    async def _fetch_messages(self, client: TelegramClient, channel, max_messages: int, progress_callback: Optional[Callable]) -> List:
        """Fetch messages from channel"""
        messages = []
        async for message in client.iter_messages(channel, limit=max_messages if max_messages > 0 else None):
            messages.append(message)
            
            if progress_callback and len(messages) % 100 == 0:
                await progress_callback(f"📡 Fetched {len(messages)} messages...")
        
        return messages
    
    async def _process_message(self, message, include_media: bool, client: TelegramClient) -> Dict[str, Any]:
        """Process a single message and extract data"""
        # Convert timezone aware datetime to UTC
        date = message.date
        if date.tzinfo is None:
            date = pytz.UTC.localize(date)
        
        processed = {
            'id': message.id,
            'date': date.isoformat(),
            'text': message.text or '',
            'sender_id': getattr(message.from_id, 'user_id', None) if message.from_id else None,
            'views': message.views,
            'forwards': message.forwards,
            'replies': message.replies.replies if message.replies else 0,
            'edit_date': message.edit_date.isoformat() if message.edit_date else None,
            'media_type': None,
            'media_file': None,
            'file_size': None,
            'duration': None,
        }
        
        # Process media
        if message.media:
            media_info = await self._process_media(message, include_media, client)
            processed.update(media_info)
        
        return processed
    
    async def _process_media(self, message, include_media: bool, client: TelegramClient) -> Dict[str, Any]:
        """Process media in message"""
        media_info = {
            'media_type': None,
            'media_file': None,
            'file_size': None,
            'duration': None,
        }
        
        if isinstance(message.media, MessageMediaPhoto):
            media_info['media_type'] = 'photo'
            if include_media:
                try:
                    filename = f"photo_{message.id}.jpg"
                    filepath = os.path.join(export_config.export_folder, 'media', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    await client.download_media(message.media, filepath)
                    media_info['media_file'] = filename
                    if os.path.exists(filepath):
                        media_info['file_size'] = os.path.getsize(filepath)
                except Exception:
                    pass  # Skip media download errors
        
        elif isinstance(message.media, MessageMediaDocument):
            document = message.media.document
            media_info['file_size'] = document.size
            
            # Determine media type
            if document.mime_type:
                if document.mime_type.startswith('video/'):
                    media_info['media_type'] = 'video'
                    # Get duration for videos
                    for attr in document.attributes:
                        if hasattr(attr, 'duration'):
                            media_info['duration'] = attr.duration
                            break
                elif document.mime_type.startswith('audio/'):
                    media_info['media_type'] = 'audio'
                    for attr in document.attributes:
                        if hasattr(attr, 'duration'):
                            media_info['duration'] = attr.duration
                            break
                elif document.mime_type.startswith('image/'):
                    media_info['media_type'] = 'image'
                else:
                    media_info['media_type'] = 'document'
            
            if include_media:
                try:
                    # Get original filename or create one
                    filename = None
                    for attr in document.attributes:
                        if hasattr(attr, 'file_name'):
                            filename = attr.file_name
                            break
                    
                    if not filename:
                        ext = 'bin'
                        if document.mime_type:
                            ext = document.mime_type.split('/')[-1]
                        filename = f"file_{message.id}.{ext}"
                    
                    filepath = os.path.join(export_config.export_folder, 'media', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    await client.download_media(message.media, filepath)
                    media_info['media_file'] = filename
                except Exception:
                    pass  # Skip media download errors
        
        return media_info
    
    async def _export_to_json(self, messages: List[Dict], filepath: str, channel):
        """Export messages to JSON format"""
        export_data = {
            'channel_info': {
                'id': channel.id,
                'title': channel.title,
                'username': channel.username,
                'description': getattr(channel, 'about', ''),
                'participants_count': getattr(channel, 'participants_count', None),
                'export_date': datetime.now().isoformat(),
            },
            'messages': messages,
            'total_messages': len(messages),
        }
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(export_data, indent=2, ensure_ascii=False))
    
    async def _export_to_csv(self, messages: List[Dict], filepath: str, channel):
        """Export messages to CSV format"""
        # Define CSV headers
        headers = [
            'id', 'date', 'text', 'sender_id', 'views', 'forwards', 'replies',
            'edit_date', 'media_type', 'media_file', 'file_size', 'duration'
        ]
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f.name, fieldnames=headers)
            await f.write(','.join(headers) + '\n')
            
            for message in messages:
                # Create row with proper escaping
                row = []
                for header in headers:
                    value = message.get(header, '')
                    if value is None:
                        value = ''
                    # Escape quotes and commas
                    value = str(value).replace('"', '""')
                    if ',' in str(value) or '"' in str(value) or '\n' in str(value):
                        value = f'"{value}"'
                    row.append(value)
                
                await f.write(','.join(row) + '\n')
    
    async def _export_to_markdown(self, messages: List[Dict], filepath: str, channel, media_files: List[str]):
        """Export messages to Markdown format"""
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            # Write header
            await f.write(f"# {channel.title}\n\n")
            
            if hasattr(channel, 'about') and channel.about:
                await f.write(f"**Description:** {channel.about}\n\n")
            
            if hasattr(channel, 'participants_count') and channel.participants_count:
                await f.write(f"**Participants:** {channel.participants_count:,}\n\n")
            
            await f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            await f.write(f"**Total Messages:** {len(messages)}\n\n")
            
            if media_files:
                await f.write(f"**Media Files:** {len(media_files)}\n\n")
            
            await f.write("---\n\n")
            
            # Write messages
            for i, message in enumerate(messages):
                # Message header
                date_str = datetime.fromisoformat(message['date'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                await f.write(f"## Message {message['id']}\n\n")
                await f.write(f"**Date:** {date_str}\n\n")
                
                if message['sender_id']:
                    await f.write(f"**Sender ID:** {message['sender_id']}\n\n")
                
                # Message text
                if message['text']:
                    # Escape markdown special characters in message text
                    text = message['text']
                    text = text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')
                    await f.write(f"{text}\n\n")
                
                # Media information
                if message['media_type']:
                    await f.write(f"**Media Type:** {message['media_type'].title()}\n\n")
                    
                    if message['media_file']:
                        await f.write(f"**Media File:** `{message['media_file']}`\n\n")
                    
                    if message['file_size']:
                        size_mb = message['file_size'] / (1024 * 1024)
                        await f.write(f"**File Size:** {size_mb:.2f} MB\n\n")
                    
                    if message['duration']:
                        duration_min = message['duration'] // 60
                        duration_sec = message['duration'] % 60
                        await f.write(f"**Duration:** {duration_min}:{duration_sec:02d}\n\n")
                
                # Statistics
                stats = []
                if message['views']:
                    stats.append(f"👁 {message['views']:,} views")
                if message['forwards']:
                    stats.append(f"📤 {message['forwards']:,} forwards")
                if message['replies']:
                    stats.append(f"💬 {message['replies']:,} replies")
                
                if stats:
                    await f.write(f"**Stats:** {' | '.join(stats)}\n\n")
                
                if message['edit_date']:
                    edit_date = datetime.fromisoformat(message['edit_date'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                    await f.write(f"**Edited:** {edit_date}\n\n")
                
                await f.write("---\n\n")
    
    async def close(self):
        """Close the Telegram client"""
        if self.client:
            await self.client.disconnect()