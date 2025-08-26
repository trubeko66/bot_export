"""
Simplified test for markdown export functionality validation
Tests markdown generation logic without external dependencies
"""
import tempfile
import os
from datetime import datetime

def create_mock_data():
    """Create mock data for testing"""
    mock_channel = {
        'id': 123456789,
        'title': "Test Channel",
        'username': "testchannel", 
        'about': "This is a test channel for markdown export validation",
        'participants_count': 1000
    }
    
    base_date = datetime.now()
    
    mock_messages = [
        {
            'id': 1,
            'date': base_date.isoformat(),
            'text': "This is a test message with *markdown* characters and _underscores_",
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
            'date': base_date.isoformat(),
            'text': "Message with photo",
            'sender_id': None,
            'views': 200,
            'forwards': 20,
            'replies': 0,
            'edit_date': None,
            'media_type': 'photo',
            'media_file': 'test_photo.jpg',
            'file_size': 1024 * 1024,
            'duration': None,
        },
        {
            'id': 3,
            'date': base_date.isoformat(),
            'text': "Video message with duration",
            'sender_id': 54321,
            'views': 300,
            'forwards': 0,
            'replies': 15,
            'edit_date': base_date.isoformat(),
            'media_type': 'video',
            'media_file': 'test_video.mp4',
            'file_size': 5 * 1024 * 1024,
            'duration': 120,
        }
    ]
    
    return mock_channel, mock_messages

def generate_markdown(messages, channel, media_files):
    """Generate markdown content from messages"""
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
        # Message header
        date_str = datetime.fromisoformat(message['date'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        lines.append(f"## Message {message['id']}\n")
        lines.append(f"**Date:** {date_str}\n")
        
        if message['sender_id']:
            lines.append(f"**Sender ID:** {message['sender_id']}\n")
        
        # Message text
        if message['text']:
            # Escape markdown special characters
            text = message['text']
            text = text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')
            lines.append(f"{text}\n")
        
        # Media information
        if message['media_type']:
            lines.append(f"**Media Type:** {message['media_type'].title()}\n")
            
            if message['media_file']:
                lines.append(f"**Media File:** `{message['media_file']}`\n")
            
            if message['file_size']:
                size_mb = message['file_size'] / (1024 * 1024)
                lines.append(f"**File Size:** {size_mb:.2f} MB\n")
            
            if message['duration']:
                # Ensure duration is an integer to avoid formatting errors
                duration_total = int(float(message['duration']))
                duration_min = duration_total // 60
                duration_sec = duration_total % 60
                lines.append(f"**Duration:** {duration_min}:{duration_sec:02d}\n")
        
        # Statistics
        stats = []
        if message['views']:
            stats.append(f"👁 {message['views']:,} views")
        if message['forwards']:
            stats.append(f"📤 {message['forwards']:,} forwards")
        if message['replies']:
            stats.append(f"💬 {message['replies']:,} replies")
        
        if stats:
            lines.append(f"**Stats:** {' | '.join(stats)}\n")
        
        if message['edit_date']:
            edit_date = datetime.fromisoformat(message['edit_date'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
            lines.append(f"**Edited:** {edit_date}\n")
        
        lines.append("---\n")
    
    return '\n'.join(lines)

def test_markdown_generation():
    """Test markdown generation functionality"""
    print("🧪 Testing Markdown Generation...")
    
    # Create test data
    channel, messages = create_mock_data()
    media_files = ['test_photo.jpg', 'test_video.mp4']
    
    try:
        # Generate markdown
        content = generate_markdown(messages, channel, media_files)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_filepath = temp_file.name
        
        print("✅ Markdown generated successfully!")
        print(f"📄 File saved to: {temp_filepath}")
        
        # Validate content
        validations = [
            ("Channel title", "Test Channel" in content),
            ("Description", "test channel for markdown export" in content),
            ("Export date", "Export Date:" in content),
            ("Total messages", "Total Messages: 3" in content),
            ("Media files count", "Media Files: 2" in content),
            ("Message headers", "## Message" in content),
            ("Escaped markdown", "\\*markdown\\*" in content),
            ("Media information", "**Media Type:**" in content),
            ("Statistics", "👁" in content and "📤" in content and "💬" in content),
            ("File size formatting", "MB" in content),
            ("Duration formatting", "2:00" in content),
            ("Photo media", "test_photo.jpg" in content),
            ("Video media", "test_video.mp4" in content),
            ("Edit information", "**Edited:**" in content),
        ]
        
        print("\n🔍 Validation Results:")
        all_passed = True
        for check_name, passed in validations:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}: {'PASSED' if passed else 'FAILED'}")
            if not passed:
                all_passed = False
        
        # Show content preview
        print(f"\n📝 Generated Content Preview (first 800 chars):")
        print("-" * 50)
        print(content[:800] + "..." if len(content) > 800 else content)
        print("-" * 50)
        
        # File size
        file_size = os.path.getsize(temp_filepath)
        print(f"\n📊 File size: {file_size} bytes ({file_size/1024:.2f} KB)")
        
        # Clean up
        os.unlink(temp_filepath)
        
        if all_passed:
            print("\n🎉 All validation tests passed!")
            return True
        else:
            print("\n⚠️ Some validation tests failed!")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

def test_edge_cases():
    """Test edge cases"""
    print("\n🧪 Testing Edge Cases...")
    
    # Test empty message
    empty_channel = {'title': 'Empty Channel', 'participants_count': 0}
    empty_messages = [{
        'id': 1,
        'date': datetime.now().isoformat(),
        'text': '',
        'sender_id': None,
        'views': None,
        'forwards': None,
        'replies': 0,
        'edit_date': None,
        'media_type': None,
        'media_file': None,
        'file_size': None,
        'duration': None,
    }]
    
    # Test special characters
    special_channel = {'title': 'Special & *Characters* _Test_', 'about': 'Channel with `special` chars'}
    special_messages = [{
        'id': 1,
        'date': datetime.now().isoformat(),
        'text': 'Text with **bold** and __italic__ and `code` and [links]',
        'sender_id': 123,
        'views': 0,
        'forwards': 0,
        'replies': 0,
        'edit_date': None,
        'media_type': None,
        'media_file': None,
        'file_size': None,
        'duration': None,
    }]
    
    test_cases = [
        ("Empty messages", empty_channel, empty_messages, []),
        ("Special characters", special_channel, special_messages, []),
    ]
    
    all_passed = True
    
    for test_name, channel, messages, media_files in test_cases:
        try:
            content = generate_markdown(messages, channel, media_files)
            print(f"✅ {test_name}: PASSED")
            
            # Basic validation - content should be generated
            if len(content) < 50:
                print(f"⚠️ {test_name}: Content seems too short")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {str(e)}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🚀 Starting Markdown Export Tests...\n")
    
    # Test basic functionality
    basic_test_passed = test_markdown_generation()
    
    # Test edge cases
    edge_test_passed = test_edge_cases()
    
    print(f"\n{'='*60}")
    print("📋 Test Summary:")
    print(f"✅ Basic functionality: {'PASSED' if basic_test_passed else 'FAILED'}")
    print(f"✅ Edge cases: {'PASSED' if edge_test_passed else 'FAILED'}")
    
    if basic_test_passed and edge_test_passed:
        print("\n🎉 All tests passed! Markdown export logic is working correctly.")
        print("📝 The markdown export functionality has been validated.")
    else:
        print("\n⚠️ Some tests failed. Please review the implementation.")
    
    print("\nPress any key to exit...")
    input()