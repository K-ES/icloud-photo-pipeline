from pathlib import Path

APPLE_ID = "ekrivonogov@inbox.ru"

# cookies вне проекта
COOKIE_DIR = Path.home() / ".icloud_cookies"
COOKIE_DIR.mkdir(exist_ok=True)

# куда скачиваем фото
DOWNLOAD_DIR = Path(r"D:\icloud_photos")

# логи
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# результат
OUT_EXCEL = DOWNLOAD_DIR / "icloud_photos_metadata.xlsx"

# имя лог-файла
LOG_FILE = LOG_DIR / "icloud_dump.log"
