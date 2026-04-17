import psutil
import platform
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.start_time = datetime.now()

    def get_uptime(self):
        delta = datetime.now() - self.start_time
        return str(delta).split('.')[0]

    def get_stats(self):
        """Собирает все данные в один словарь"""
        return {
            "node": platform.node(),
            "cpu": psutil.cpu_percent(interval=None),
            "ram": psutil.virtual_memory(),
            "net": psutil.net_io_counters(),
            "temp": self.get_temperatures()
        }

    def get_temperatures(self):
        if hasattr(psutil, "sensors_temperatures"):
            return psutil.sensors_temperatures()
        return {}

    @staticmethod
    def format_size(bytes):
        for unit in ['', 'K', 'M', 'G', 'T']:
            if abs(bytes) < 1024:
                return f"{bytes:.2f}{unit}B"
            bytes /= 1024