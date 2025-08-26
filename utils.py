"""
Utility functions for Telegram Channel Export Bot
Additional helper functions and tools
"""
import os
import json
import shutil
from datetime import datetime
from typing import List, Dict, Any

def cleanup_old_exports(export_folder: str = "exports", days_old: int = 7):
    """Clean up export files older than specified days"""
    if not os.path.exists(export_folder):
        return
    
    current_time = datetime.now()
    files_removed = 0
    
    for filename in os.listdir(export_folder):
        if filename == "media":  # Skip media directory
            continue
            
        file_path = os.path.join(export_folder, filename)
        
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            age_days = (current_time - file_time).days
            
            if age_days > days_old:
                os.remove(file_path)
                files_removed += 1
    
    return files_removed

def get_export_statistics(export_folder: str = "exports") -> Dict[str, Any]:
    """Get statistics about exports"""
    stats = {
        'total_files': 0,
        'formats': {'json': 0, 'csv': 0, 'md': 0},
        'total_size_mb': 0,
        'media_files': 0,
        'oldest_export': None,
        'newest_export': None
    }
    
    if not os.path.exists(export_folder):
        return stats
    
    for filename in os.listdir(export_folder):
        if filename == "media":
            # Count media files
            media_path = os.path.join(export_folder, filename)
            if os.path.isdir(media_path):
                stats['media_files'] = len(os.listdir(media_path))
            continue
        
        file_path = os.path.join(export_folder, filename)
        
        if os.path.isfile(file_path):
            stats['total_files'] += 1
            
            # File size
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            stats['total_size_mb'] += size_mb
            
            # File format
            ext = filename.lower().split('.')[-1]
            if ext in stats['formats']:
                stats['formats'][ext] += 1
            
            # File dates
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            
            if stats['oldest_export'] is None or file_time < stats['oldest_export']:
                stats['oldest_export'] = file_time
            
            if stats['newest_export'] is None or file_time > stats['newest_export']:
                stats['newest_export'] = file_time
    
    # Round size
    stats['total_size_mb'] = round(stats['total_size_mb'], 2)
    
    return stats

def validate_export_file(file_path: str) -> Dict[str, Any]:
    """Validate an export file and return information"""
    result = {
        'valid': False,
        'format': None,
        'size_mb': 0,
        'message_count': 0,
        'error': None
    }
    
    if not os.path.exists(file_path):
        result['error'] = "File does not exist"
        return result
    
    result['size_mb'] = round(os.path.getsize(file_path) / (1024 * 1024), 2)
    
    # Determine format
    ext = file_path.lower().split('.')[-1]
    result['format'] = ext
    
    try:
        if ext == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'messages' in data and isinstance(data['messages'], list):
                    result['message_count'] = len(data['messages'])
                    result['valid'] = True
                else:
                    result['error'] = "Invalid JSON structure"
        
        elif ext == 'csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                result['message_count'] = max(0, len(lines) - 1)  # Subtract header
                result['valid'] = True
        
        elif ext == 'md':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Count message headers
                result['message_count'] = content.count('## Message')
                result['valid'] = True
        
        else:
            result['error'] = f"Unsupported format: {ext}"
    
    except Exception as e:
        result['error'] = str(e)
    
    return result

def create_backup(source_folder: str = "exports", backup_folder: str = "backups"):
    """Create a backup of export files"""
    if not os.path.exists(source_folder):
        return False
    
    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_folder, f"export_backup_{timestamp}")
    
    try:
        shutil.copytree(source_folder, backup_path)
        return backup_path
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_channel_info_from_export(file_path: str) -> Dict[str, Any]:
    """Extract channel information from export file"""
    info = {
        'title': 'Unknown',
        'username': 'Unknown',
        'description': '',
        'participants': 0,
        'export_date': 'Unknown'
    }
    
    if not os.path.exists(file_path):
        return info
    
    try:
        ext = file_path.lower().split('.')[-1]
        
        if ext == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'channel_info' in data:
                    channel = data['channel_info']
                    info.update({
                        'title': channel.get('title', 'Unknown'),
                        'username': channel.get('username', 'Unknown'),
                        'description': channel.get('description', ''),
                        'participants': channel.get('participants_count', 0),
                        'export_date': channel.get('export_date', 'Unknown')
                    })
        
        elif ext == 'md':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Extract title (first line)
                if lines and lines[0].startswith('# '):
                    info['title'] = lines[0][2:].strip()
                
                # Extract other info from markdown
                for line in lines:
                    if '**Description:**' in line:
                        info['description'] = line.split('**Description:**')[1].strip()
                    elif '**Participants:**' in line:
                        participants_str = line.split('**Participants:**')[1].strip()
                        # Remove commas and convert to int
                        try:
                            info['participants'] = int(participants_str.replace(',', ''))
                        except:
                            pass
                    elif '**Export Date:**' in line:
                        info['export_date'] = line.split('**Export Date:**')[1].strip()
    
    except Exception as e:
        print(f"Error extracting channel info: {e}")
    
    return info

if __name__ == "__main__":
    print("🔧 Telegram Channel Export Bot - Utilities")
    print()
    
    # Display statistics
    print("📊 Export Statistics:")
    stats = get_export_statistics()
    print(f"   📁 Total files: {stats['total_files']}")
    print(f"   📝 JSON: {stats['formats']['json']}, CSV: {stats['formats']['csv']}, MD: {stats['formats']['md']}")
    print(f"   💾 Total size: {stats['total_size_mb']} MB")
    print(f"   🎥 Media files: {stats['media_files']}")
    
    if stats['newest_export']:
        print(f"   📅 Latest export: {stats['newest_export'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    print()
    print("✅ Utilities loaded successfully!")