import os
import tarfile
import zipfile
import urllib.request
import platform
import subprocess


class ServiceGuard:
    def __init__(self):
        self.version = "1.9.0"
        self.os_type = platform.system().lower()  # 'windows' или 'linux'
        self.process = None

        # Определяем имя файла и ссылку в зависимости от ОС
        if self.os_type == "windows":
            self.bin_name = "mediamtx.exe"
            self.extension = "zip"
            self.url = f"https://github.com/bluenviron/mediamtx/releases/download/v{self.version}/mediamtx_v{self.version}_windows_amd64.zip"
        else:
            self.bin_name = "mediamtx"
            self.extension = "tar.gz"
            self.url = f"https://github.com/bluenviron/mediamtx/releases/download/v{self.version}/mediamtx_v{self.version}_linux_amd64.tar.gz"

    def download_engine(self):
        if not os.path.exists(self.bin_name):
            print(f"📦 ОС: {self.os_type.upper()}. Качаем MediaMTX...")
            archive_path = f"mediamtx.{self.extension}"
            urllib.request.urlretrieve(self.url, archive_path)

            # Распаковка зависит от формата
            if self.extension == "zip":
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(".")
            else:
                with tarfile.open(archive_path, "r:gz") as tar:
                    tar.extractall()

            os.remove(archive_path)
            if self.os_type != "windows":
                os.chmod(self.bin_name, 0o755)
            print("✅ Двигатель готов!")

    def start_engine(self):
        if not self.process or self.process.poll() is not None:
            # Путь к запуску
            cmd = f"./{self.bin_name}" if self.os_type != "windows" else self.bin_name
            try:
                self.process = subprocess.Popen(
                    [cmd],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"🚀 Стриминг-сервер запущен ({self.os_type})")
            except Exception as e:
                print(f"❌ Ошибка запуска: {e}")

    def stop_engine(self):
        if self.process:
            self.process.terminate()
            print("🛑 Стриминг-сервер остановлен.")