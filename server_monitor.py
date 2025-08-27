"""
Server Monitoring Module for Telegram Channel Export Bot
Provides system statistics, process monitoring, and resource usage information
"""
import os
import psutil
import shutil
import time
import platform
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

class ServerMonitor:
    """Server monitoring class with system statistics"""
    
    def __init__(self):
        self.start_time = datetime.now()
        
    def get_system_info(self) -> Dict[str, str]:
        """Get basic system information"""
        info = {
            'os': platform.system(),
            'os_version': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node(),
            'python_version': platform.python_version()
        }
        return info
    
    def get_cpu_usage(self) -> Dict[str, float]:
        """Get CPU usage statistics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        load_avg = None
        if hasattr(os, 'getloadavg'):
            try:
                load_avg = os.getloadavg()
            except:
                load_avg = None
        
        return {
            'usage_percent': cpu_percent,
            'core_count': float(cpu_count or 0),
            'frequency_mhz': cpu_freq.current if cpu_freq else 0.0,
            'load_average_1m': load_avg[0] if load_avg else 0.0,
            'load_average_5m': load_avg[1] if load_avg else 0.0,
            'load_average_15m': load_avg[2] if load_avg else 0.0
        }
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage statistics"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_gb': memory.total / (1024**3),
            'used_gb': memory.used / (1024**3),
            'available_gb': memory.available / (1024**3),
            'percent_used': memory.percent,
            'swap_total_gb': swap.total / (1024**3),
            'swap_used_gb': swap.used / (1024**3),
            'swap_percent': swap.percent
        }
    
    def get_disk_usage(self) -> Dict[str, Dict[str, float]]:
        """Get disk usage for all mounted drives"""
        disk_info = {}
        
        # Get all disk partitions
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    'total_gb': usage.total / (1024**3),
                    'used_gb': usage.used / (1024**3),
                    'free_gb': usage.free / (1024**3),
                    'percent_used': (usage.used / usage.total) * 100,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype
                }
            except PermissionError:
                continue
        
        return disk_info
    
    def get_network_usage(self) -> Dict[str, Dict[str, float]]:
        """Get network interface statistics"""
        # Get initial values
        net_io_start = psutil.net_io_counters(pernic=True)
        time.sleep(1)  # Wait 1 second
        net_io_end = psutil.net_io_counters(pernic=True)
        
        network_info = {}
        
        for interface, stats_start in net_io_start.items():
            if interface in net_io_end:
                stats_end = net_io_end[interface]
                
                # Calculate bytes per second
                bytes_sent_per_sec = stats_end.bytes_sent - stats_start.bytes_sent
                bytes_recv_per_sec = stats_end.bytes_recv - stats_start.bytes_recv
                
                network_info[interface] = {
                    'bytes_sent_total': stats_end.bytes_sent,
                    'bytes_recv_total': stats_end.bytes_recv,
                    'bytes_sent_per_sec': bytes_sent_per_sec,
                    'bytes_recv_per_sec': bytes_recv_per_sec,
                    'packets_sent': stats_end.packets_sent,
                    'packets_recv': stats_end.packets_recv,
                    'errors_in': stats_end.errin,
                    'errors_out': stats_end.errout,
                    'drops_in': stats_end.dropin,
                    'drops_out': stats_end.dropout
                }
        
        return network_info
    
    def get_top_processes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top processes by CPU and memory usage"""
        processes = []
        
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info', 'create_time', 'status']):
            try:
                # Get CPU percent (this will return 0.0 for the first call)
                cpu_percent = process.info.get('cpu_percent', 0.0)
                if cpu_percent is None:
                    cpu_percent = 0.0
                
                memory_percent = process.info.get('memory_percent', 0.0)
                if memory_percent is None:
                    memory_percent = 0.0
                
                memory_info = process.info.get('memory_info')
                memory_mb = memory_info.rss / (1024 * 1024) if memory_info else 0
                
                create_time = process.info.get('create_time')
                uptime = datetime.now() - datetime.fromtimestamp(create_time) if create_time else timedelta(0)
                
                processes.append({
                    'pid': process.info['pid'],
                    'name': process.info['name'],
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent,
                    'memory_mb': memory_mb,
                    'status': process.info.get('status', 'unknown'),
                    'uptime': str(uptime).split('.')[0]  # Remove microseconds
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort by CPU usage first, then by memory usage
        processes.sort(key=lambda x: (x['cpu_percent'], x['memory_percent']), reverse=True)
        
        return processes[:limit]
    
    def get_uptime(self) -> Dict[str, str]:
        """Get system and bot uptime"""
        # System uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        system_uptime = datetime.now() - boot_time
        
        # Bot uptime
        bot_uptime = datetime.now() - self.start_time
        
        return {
            'system_uptime': str(system_uptime).split('.')[0],
            'bot_uptime': str(bot_uptime).split('.')[0],
            'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def format_bytes(self, bytes_value: float) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def get_temperature(self) -> Optional[Dict[str, float]]:
        """Get system temperature (if available)"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                temperature_info = {}
                for name, entries in temps.items():
                    if entries:
                        temperature_info[name] = entries[0].current
                return temperature_info
        except:
            pass
        return None
    
    def get_battery_info(self) -> Optional[Dict[str, Any]]:
        """Get battery information (if available)"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'plugged_in': battery.power_plugged,
                    'time_left': str(timedelta(seconds=battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unknown"
                }
        except:
            pass
        return None