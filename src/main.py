import subprocess
import platform
import sys
import os
from datetime import datetime
import time
import requests
import psutil
from monitor import SystemMonitor
from guard import ServiceGuard


def link_creating (stream_path ="mystream"):
    try:
        Ip_check_url = "https://api.ipify.org"
        response = requests.get(Ip_check_url, timeout=5)
        ip = response.text
        user = "admin"
        password = "12345678"
        link = (f"rtsp://{user}:{password}@{ip}:8554/{path}")
        return link
    except Exception as e:
        return f"Не удалось создать ссылку: {e}"



def check_dependencies():
    try:
        import psutil
        import subprocess
        import platform
        import sys
        import os
        from datetime import datetime
        import time
        import requests
        import psutil
        from monitor import SystemMonitor
        from guard import ServiceGuard
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        print("✅ Done.")


class FrankenApp:
    def __init__(self):
        # Инициализируем монитор и охранника сервиса
        self.monitor = SystemMonitor()
        self.guard = ServiceGuard()

    def render(self):
        # Очистка экрана
        os.system('cls' if os.name == 'nt' else 'clear')

        # Берем данные из монитора
        stats = self.monitor.get_stats()
        uptime = self.monitor.get_uptime()

        print(f" {stats['node']} ".center(50, "="))
        print(f"Uptime: {uptime} | Python: {platform.python_version()}")
        print("-" * 50)

        # CPU
        bar = "#" * int(stats['cpu'] / 5)
        print(f"CPU: [{bar:<20}] {stats['cpu']}%")

        # RAM
        ram = stats['ram']
        print(f"RAM: {self.monitor.format_size(ram.used)} / {self.monitor.format_size(ram.total)} ({ram.percent}%)")

        # Network
        net = stats['net']
        print(f"Net Sent: {self.monitor.format_size(net.bytes_sent)}")
        print(f"Net Recv: {self.monitor.format_size(net.bytes_recv)}")

        # Температура
        if stats['temp']:
            print("-" * 50)
            for name, entries in stats['temp'].items():
                for entry in entries:
                    print(f"🌡 {entry.label or name}: {entry.current}°C")

        print("-" * 50)
        print("Press Ctrl+C to stop FrankenStream")

    def run(self):
        # 1. Сначала готовим движок (скачиваем, если надо)
        self.guard.download_engine()

        # 2. Запускаем стриминг-сервер
        self.guard.start_engine()

        try:
            while True:
                self.render()
                time.sleep(1)
        except KeyboardInterrupt:
            # 3. При выходе гасим сервер, чтобы он не висел в памяти
            self.guard.stop_engine()
            print("\n[!] FrankenStream stopped.")


if __name__ == "__main__":
    check_dependencies()
    app = FrankenApp()
    app.run()