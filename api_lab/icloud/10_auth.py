from pyicloud import PyiCloudService
from pathlib import Path

from config import APPLE_ID, COOKIE_DIR

# ==============================
# AUTH / SESSION INIT
# ==============================

def auth():
    print("Инициализация iCloud API...")

    api = PyiCloudService(
        APPLE_ID,
        cookie_directory=str(COOKIE_DIR)
    )

    # cookies живые — сразу выходим
    if not api.requires_2fa and api.is_trusted_session:
        print("Сессия уже активна, авторизация не требуется")
        return api

    # если cookies есть, но сессия не доверенная
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

        if not api.is_trusted_session:
            api.trust_session()

    print("Авторизация завершена, сессия сохранена")
    return api


if __name__ == "__main__":
    auth()
