from pyicloud import PyiCloudService
from config import APPLE_ID, COOKIE_DIR

def check_session():
    api = PyiCloudService(
        APPLE_ID,
        cookie_directory=str(COOKIE_DIR)
    )

    print("requires_2fa:", api.requires_2fa)
    print("is_trusted_session:", api.is_trusted_session)

    return api


if __name__ == "__main__":
    check_session()
