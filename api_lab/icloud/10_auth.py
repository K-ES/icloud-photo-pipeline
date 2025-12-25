from pyicloud import PyiCloudService
from pathlib import Path

APPLE_ID = "ekrivonogov@inbox.ru"

# ==============================
# ХРАНЕНИЕ COOKIES (ВНЕ ПРОЕКТА)
# ==============================
# Cookies сохраняются в домашнем каталоге пользователя.
# Windows: C:\Users\<username>\.icloud_cookies
# Linux/macOS: /home/<username>/.icloud_cookies
#
# Эта папка НЕ находится в репозитории и НЕ может быть закоммичена.
COOKIE_DIR = Path.home() / ".icloud_cookies"
COOKIE_DIR.mkdir(exist_ok=True)

print("Инициализация iCloud API...")

api = PyiCloudService(
    APPLE_ID,
    cookie_directory=str(COOKIE_DIR)
)

# если cookies живые — выходим без авторизации
if not api.requires_2fa and api.is_trusted_session:
    print("Сессия уже активна, авторизация не требуется")
    exit(0)

# если требуется повторный логин
if not api.is_trusted_session:
    password = input("iCloud password: ")
    api = PyiCloudService(
        APPLE_ID,
        password=password,
        cookie_directory=str(COOKIE_DIR)
    )

# 2FA
if api.requires_2fa:
    code = input("Enter 2FA code: ")
    if not api.validate_2fa_code(code):
        raise RuntimeError("Неверный код 2FA")

    # помечаем сессию как доверенную
    if not api.is_trusted_session:
        api.trust_session()

print("Авторизация завершена, сессия сохранена")
