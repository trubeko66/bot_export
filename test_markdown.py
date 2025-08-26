"""
Test script for markdown export functionality
Tests the markdown export without requiring actual Telegram API calls
"""
import asyncio
import os
import tempfile
from datetime import datetime
from exporters import ChannelExporter

class MockChannel:
    """Mock channel object for testing"""
    def __init__(self):
        self.id = 123456789
        self.title = "Test Channel"
        self.username = "testchannel"
        self.about = "This is a test channel for markdown export validation"
        self.participants_count = 1000

class MockMessage:
    """Mock message object for testing"""
    def __init__(self, msg_id, text, date, media_type=None):
        self.id = msg_id
        self.text = text
        self.date = date
        self.from_id = None
        self.views = 100
        self.forwards = 10
        self.replies = 5
        self.edit_date = None
        self.media = None

async def test_markdown_export():
    """Test markdown export functionality"""
    print("🧪 Testing Markdown Export Functionality...")
    
    # Create test data
    test_messages = []
    base_date = datetime.now()
    
    # Create sample messages
    sample_texts = [
        "This is a test message with *markdown* characters and _underscores_",
        "Another message with `code` and special characters: @#$%^&*()",
        "Message with emojis: 🚀 🎉 💯 and multiple lines\nSecond line\nThird line",
        "Empty media message",
        "Final test message with numbers: 12345 and symbols: <>{}[]"
    ]
    
    for i, text in enumerate(sample_texts):
        processed_msg = {
            'id': i + 1,
            'date': base_date.isoformat(),
            'text': text,
            'sender_id': 12345 if i % 2 == 0 else None,
            'views': (i + 1) * 100,
            'forwards': (i + 1) * 10,
            'replies': i * 2,
            'edit_date': base_date.isoformat() if i == 2 else None,
            'media_type': 'photo' if i == 1 else 'video' if i == 3 else None,
            'media_file': f'test_file_{i}.jpg' if i == 1 else f'test_video_{i}.mp4' if i == 3 else None,
            'file_size': 1024 * 1024 * (i + 1) if i in [1, 3] else None,
            'duration': 120 if i == 3 else None,
        }
        test_messages.append(processed_msg)
    
    # Create temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
        temp_filepath = temp_file.name
    
    try:
        # Create exporter instance
        exporter = ChannelExporter()
        mock_channel = MockChannel()
        media_files = ['test_file_1.jpg', 'test_video_3.mp4']
        
        # Test markdown export
        await exporter._export_to_markdown(test_messages, temp_filepath, mock_channel, media_files)
        
        # Read and validate the exported file
        with open(temp_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Markdown export completed successfully!")
        print("\n📝 Generated Content Preview:")
        print("-" * 50)
        print(content[:1000] + "..." if len(content) > 1000 else content)
        print("-" * 50)
        
        # Validate content
        validations = [
            ("Channel title", "Test Channel" in content),
            ("Channel description", "test channel for markdown export" in content),
            ("Export date", "Export Date:" in content),
            ("Total messages", "Total Messages: 5" in content),
            ("Media files count", "Media Files: 2" in content),
            ("Message headers", "## Message" in content),
            ("Escaped markdown", "\\*markdown\\*" in content),
            ("Media information", "**Media Type:**" in content),
            ("Statistics", "👁" in content and "📤" in content and "💬" in content),
            ("File size formatting", "MB" in content),
            ("Duration formatting", ":" in content and any("Duration" in line for line in content.split('\n'))),
        ]
        
        print("\n🔍 Validation Results:")
        all_passed = True
        for check_name, passed in validations:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}: {'PASSED' if passed else 'FAILED'}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 All validation tests passed!")
        else:
            print("\n⚠️ Some validation tests failed!")
        
        # Test file size
        file_size = os.path.getsize(temp_filepath)
        print(f"\n📊 Generated file size: {file_size} bytes ({file_size/1024:.2f} KB)")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
    
    finally:
        # Clean up
        if os.path.exists(temp_filepath):
            os.unlink(temp_filepath)

async def test_edge_cases():
    """Test edge cases for markdown export"""
    print("\n🧪 Testing Edge Cases...")
    
    # Test with empty messages
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
    
    # Test with special characters
    special_messages = [{
        'id': 2,
        'date': datetime.now().isoformat(),
        'text': 'Special chars: **bold** __italic__ `code` [link](url) > quote',
        'sender_id': 12345,
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
        ("Empty messages", empty_messages),
        ("Special characters", special_messages),
    ]
    
    exporter = ChannelExporter()
    mock_channel = MockChannel()
    
    all_passed = True
    
    for test_name, messages in test_cases:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
                temp_filepath = temp_file.name
            
            await exporter._export_to_markdown(messages, temp_filepath, mock_channel, [])
            
            with open(temp_filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ {test_name}: PASSED")
            
            os.unlink(temp_filepath)
            
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {str(e)}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    async def main():
        print("🚀 Starting Markdown Export Tests...\n")
        
        # Test basic functionality
        basic_test_passed = await test_markdown_export()
        
        # Test edge cases
        edge_test_passed = await test_edge_cases()
        
        print(f"\n{'='*50}")
        print("📋 Test Summary:")
        print(f"✅ Basic functionality: {'PASSED' if basic_test_passed else 'FAILED'}")
        print(f"✅ Edge cases: {'PASSED' if edge_test_passed else 'FAILED'}")
        
        if basic_test_passed and edge_test_passed:
            print("\n🎉 All tests passed! Markdown export is working correctly.")
        else:
            print("\n⚠️ Some tests failed. Please review the implementation.")
    
    asyncio.run(main())