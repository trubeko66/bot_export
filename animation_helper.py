"""
Animation utilities for server monitoring displays
Provides animated progress bars, loading animations, and visual effects
"""
import asyncio
from typing import List
from telegram import Update
from telegram.constants import ParseMode

class AnimationHelper:
    """Helper class for creating animated displays"""
    
    def __init__(self):
        self.loading_frames = [
            "🔄 Loading",
            "🔄 Loading.",
            "🔄 Loading..",
            "🔄 Loading..."
        ]
        
        self.progress_frames = [
            "█░░░░░░░░░ 10%",
            "██░░░░░░░░ 20%", 
            "███░░░░░░░ 30%",
            "████░░░░░░ 40%",
            "█████░░░░░ 50%",
            "██████░░░░ 60%",
            "███████░░░ 70%",
            "████████░░ 80%",
            "█████████░ 90%",
            "██████████ 100%"
        ]
        
        self.cpu_bar_chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        
    def get_progress_bar(self, percentage: float, width: int = 10) -> str:
        """Generate a progress bar based on percentage"""
        filled = int((percentage / 100) * width)
        empty = width - filled
        return "█" * filled + "░" * empty + f" {percentage:.1f}%"
        
    def get_cpu_visual(self, cpu_percent: float) -> str:
        """Generate visual CPU usage indicator"""
        level = min(int((cpu_percent / 100) * len(self.cpu_bar_chars)), len(self.cpu_bar_chars) - 1)
        return self.cpu_bar_chars[level] * 8
        
    def get_memory_visual(self, memory_percent: float) -> str:
        """Generate visual memory usage indicator"""
        if memory_percent < 25:
            color = "🟢"
        elif memory_percent < 50:
            color = "🟡"
        elif memory_percent < 75:
            color = "🟠"
        else:
            color = "🔴"
        
        bars = int(memory_percent / 10)
        return color + "█" * bars + "░" * (10 - bars)
        
    def get_disk_visual(self, disk_percent: float) -> str:
        """Generate visual disk usage indicator"""
        if disk_percent < 60:
            return "💚"
        elif disk_percent < 80:
            return "💛"
        else:
            return "❤️"
            
    def get_network_arrows(self, sent_bytes: float, recv_bytes: float) -> str:
        """Generate network activity arrows"""
        up_arrow = "⬆️" if sent_bytes > 1024 else "↗️"
        down_arrow = "⬇️" if recv_bytes > 1024 else "↘️"
        return f"{up_arrow}{down_arrow}"
        
    def format_uptime(self, uptime_str: str) -> str:
        """Format uptime with nice icons"""
        parts = uptime_str.split(", ")
        formatted_parts = []
        
        for part in parts:
            if "day" in part:
                formatted_parts.append(f"📅 {part}")
            elif ":" in part:  # Time format
                formatted_parts.append(f"⏰ {part}")
                
        return " ".join(formatted_parts) if formatted_parts else f"⏰ {uptime_str}"
        
    def get_temperature_emoji(self, temp: float) -> str:
        """Get temperature emoji based on value"""
        if temp < 40:
            return "❄️"
        elif temp < 60:
            return "🌡️"
        elif temp < 80:
            return "🔥"
        else:
            return "🚨"
            
    def get_load_indicator(self, load_avg: float, cpu_count: float) -> str:
        """Get load average indicator"""
        load_percent = (load_avg / cpu_count) * 100
        
        if load_percent < 50:
            return "✅ Low"
        elif load_percent < 80:
            return "⚠️ Medium" 
        else:
            return "🚨 High"
            
    def animate_text(self, base_text: str, frame: int) -> str:
        """Add animation to text"""
        animation_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        char = animation_chars[frame % len(animation_chars)]
        return f"{char} {base_text}"
        
    async def show_loading_animation(self, update: Update, base_message: str, duration: int = 3):
        """Show animated loading message"""
        for i in range(duration * 2):  # 2 frames per second
            frame_text = self.animate_text(base_message, i)
            try:
                await update.callback_query.edit_message_text(
                    frame_text,
                    parse_mode=ParseMode.HTML
                )
                await asyncio.sleep(0.5)
            except:
                break  # Stop if message can't be edited
                
    def get_status_emoji(self, status: str) -> str:
        """Get emoji for process status"""
        status_map = {
            'running': '🟢',
            'sleeping': '😴',
            'disk-sleep': '💤',
            'stopped': '⏹️',
            'tracing-stop': '🔍',
            'zombie': '🧟',
            'dead': '💀',
            'wake-kill': '⚡',
            'waking': '👁️'
        }
        return status_map.get(status.lower(), '❓')
        
    def format_bytes_with_color(self, bytes_value: float) -> str:
        """Format bytes with color indicators"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                if unit in ['GB', 'TB']:
                    return f"🔴 {bytes_value:.1f} {unit}"
                elif unit == 'MB':
                    return f"🟡 {bytes_value:.1f} {unit}"
                else:
                    return f"🟢 {bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"🔴 {bytes_value:.1f} PB"
        
    def create_sparkline(self, values: List[float], width: int = 8) -> str:
        """Create a simple sparkline from values"""
        if not values:
            return "No data"
            
        min_val = min(values)
        max_val = max(values)
        
        if max_val == min_val:
            return "▄" * width
            
        chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        sparkline = ""
        
        for val in values[-width:]:  # Take last 'width' values
            normalized = (val - min_val) / (max_val - min_val)
            char_index = min(int(normalized * (len(chars) - 1)), len(chars) - 1)
            sparkline += chars[char_index]
            
        return sparkline
        
    def get_system_health_emoji(self, cpu_percent: float, memory_percent: float, disk_percent: float) -> str:
        """Get overall system health emoji"""
        avg_usage = (cpu_percent + memory_percent + disk_percent) / 3
        
        if avg_usage < 30:
            return "💚 Excellent"
        elif avg_usage < 50:
            return "💛 Good"
        elif avg_usage < 70:
            return "🧡 Fair"
        elif avg_usage < 85:
            return "❤️ Poor"
        else:
            return "🚨 Critical"