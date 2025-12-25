from pyicloud import PyiCloudService
from pathlib import Path

APPLE_ID = "ekrivonogov@inbox.ru"

# cookies вне проекта
COOKIE_DIR = Path.home() / ".icloud_cookies"
COOKIE_DIR.mkdir(exist_ok=True)

api = PyiCloudService(
    APPLE_ID,
    cookie_directory=str(COOKIE_DIR)
)

print("requires_2fa:", api.requires_2fa)
print("is_trusted_session:", api.is_trusted_session)
