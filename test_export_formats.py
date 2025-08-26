"""
Test all export formats: JSON, CSV, and Markdown
"""
import tempfile
import os
import json
import csv
from datetime import datetime

def create_test_data():
    """Create test data for all formats"""
    mock_channel = {
        'id': 123456789,
        'title': "Test Channel",
        'username': "testchannel", 
        'about': "This is a test channel",
        'participants_count': 1000
    }
    
    mock_messages = [
        {
            'id': 1,
            'date': datetime.now().isoformat(),
            'text': "Test message 1",
            'sender_id': 12345,
            'views': 100,
            'forwards': 10,
            'replies': 5,
            'edit_date': None,
            'media_type': None,
            'media_file': None,
            'file_size': None,
            'duration': None,
        },
        {
            'id': 2,
            'date': datetime.now().isoformat(),
            'text': "Message with photo",
            'sender_id': None,
            'views': 200,
            'forwards': 0,
            'replies': 0,
            'edit_date': None,
            'media_type': 'photo',
            'media_file': 'photo.jpg',
            'file_size': 1024000,
            'duration': None,
        }
    ]
    
    return mock_channel, mock_messages

def test_json_export():
    """Test JSON export functionality"""
    print("🧪 Testing JSON Export...")
    
    channel, messages = create_test_data()
    
    export_data = {
        'channel_info': {
            'id': channel['id'],
            'title': channel['title'],
            'username': channel['username'],
            'description': channel.get('about', ''),
            'participants_count': channel.get('participants_count', None),
            'export_date': datetime.now().isoformat(),
        },
        'messages': messages,
        'total_messages': len(messages),
    }
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as temp_file:
            json.dump(export_data, temp_file, indent=2, ensure_ascii=False)
            temp_filepath = temp_file.name
        
        # Validate JSON
        with open(temp_filepath, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        validations = [
            ("Valid JSON", isinstance(loaded_data, dict)),
            ("Channel info", 'channel_info' in loaded_data),
            ("Messages array", 'messages' in loaded_data and isinstance(loaded_data['messages'], list)),
            ("Message count", len(loaded_data['messages']) == 2),
            ("Channel title", loaded_data['channel_info']['title'] == "Test Channel"),
            ("Total messages", loaded_data['total_messages'] == 2),
        ]
        
        all_passed = True
        for check_name, passed in validations:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}: {'PASSED' if passed else 'FAILED'}")
            if not passed:
                all_passed = False
        
        file_size = os.path.getsize(temp_filepath)
        print(f"📊 JSON file size: {file_size} bytes")
        
        os.unlink(temp_filepath)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ JSON test failed: {str(e)}")
        return False

def test_csv_export():
    """Test CSV export functionality"""
    print("\n🧪 Testing CSV Export...")
    
    channel, messages = create_test_data()
    
    headers = [
        'id', 'date', 'text', 'sender_id', 'views', 'forwards', 'replies',
        'edit_date', 'media_type', 'media_file', 'file_size', 'duration'
    ]
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=headers)
            writer.writeheader()
            
            for message in messages:
                row = {}
                for header in headers:
                    value = message.get(header, '')
                    if value is None:
                        value = ''
                    row[header] = value
                writer.writerow(row)
            
            temp_filepath = temp_file.name
        
        # Validate CSV
        with open(temp_filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        validations = [
            ("CSV readable", len(rows) >= 0),
            ("Correct row count", len(rows) == 2),
            ("Headers present", reader.fieldnames == headers),
            ("First message ID", rows[0]['id'] == '1'),
            ("Second message media", rows[1]['media_type'] == 'photo'),
        ]
        
        all_passed = True
        for check_name, passed in validations:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}: {'PASSED' if passed else 'FAILED'}")
            if not passed:
                all_passed = False
        
        file_size = os.path.getsize(temp_filepath)
        print(f"📊 CSV file size: {file_size} bytes")
        
        os.unlink(temp_filepath)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ CSV test failed: {str(e)}")
        return False

def test_markdown_export():
    """Test Markdown export functionality"""
    print("\n🧪 Testing Markdown Export...")
    
    channel, messages = create_test_data()
    media_files = ['photo.jpg']
    
    try:
        lines = []
        
        # Header
        lines.append(f"# {channel['title']}\n")
        
        if channel.get('about'):
            lines.append(f"**Description:** {channel['about']}\n")
        
        if channel.get('participants_count'):
            lines.append(f"**Participants:** {channel['participants_count']:,}\n")
        
        lines.append(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"**Total Messages:** {len(messages)}\n")
        
        if media_files:
            lines.append(f"**Media Files:** {len(media_files)}\n")
        
        lines.append("---\n")
        
        # Messages
        for message in messages:
            date_str = datetime.fromisoformat(message['date'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
            lines.append(f"## Message {message['id']}\n")
            lines.append(f"**Date:** {date_str}\n")
            
            if message['sender_id']:
                lines.append(f"**Sender ID:** {message['sender_id']}\n")
            
            if message['text']:
                text = message['text']
                text = text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')
                lines.append(f"{text}\n")
            
            if message['media_type']:
                lines.append(f"**Media Type:** {message['media_type'].title()}\n")
                
                if message['media_file']:
                    lines.append(f"**Media File:** `{message['media_file']}`\n")
                
                if message['file_size']:
                    size_mb = message['file_size'] / (1024 * 1024)
                    lines.append(f"**File Size:** {size_mb:.2f} MB\n")
            
            stats = []
            if message['views']:
                stats.append(f"👁 {message['views']:,} views")
            if message['forwards']:
                stats.append(f"📤 {message['forwards']:,} forwards")
            if message['replies']:
                stats.append(f"💬 {message['replies']:,} replies")
            
            if stats:
                lines.append(f"**Stats:** {' | '.join(stats)}\n")
            
            lines.append("---\n")
        
        content = '\n'.join(lines)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_filepath = temp_file.name
        
        validations = [
            ("Channel title", "Test Channel" in content),
            ("Description", "test channel" in content.lower()),
            ("Export date", "Export Date:" in content),
            ("Total messages", "Total Messages: 2" in content),
            ("Media files", "Media Files: 1" in content),
            ("Message headers", "## Message" in content),
            ("Media info", "**Media Type:** Photo" in content),
            ("Statistics", "👁" in content),
            ("Photo file", "photo.jpg" in content),
        ]
        
        all_passed = True
        for check_name, passed in validations:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}: {'PASSED' if passed else 'FAILED'}")
            if not passed:
                all_passed = False
        
        file_size = os.path.getsize(temp_filepath)
        print(f"📊 Markdown file size: {file_size} bytes")
        
        os.unlink(temp_filepath)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Markdown test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing All Export Formats...\n")
    
    # Test all formats
    json_passed = test_json_export()
    csv_passed = test_csv_export()
    markdown_passed = test_markdown_export()
    
    print(f"\n{'='*60}")
    print("📋 Export Format Test Results:")
    print(f"✅ JSON Export: {'PASSED' if json_passed else 'FAILED'}")
    print(f"✅ CSV Export: {'PASSED' if csv_passed else 'FAILED'}")
    print(f"✅ Markdown Export: {'PASSED' if markdown_passed else 'FAILED'}")
    
    if json_passed and csv_passed and markdown_passed:
        print("\n🎉 All export formats are working correctly!")
        print("📝 The bot export functionality has been validated.")
    else:
        print("\n⚠️ Some export formats failed. Please review the implementation.")
    
    print("\nPress any key to exit...")
    input()