from pyicloud import PyiCloudService
from pyicloud.exceptions import (
    PyiCloudFailedLoginException,
    PyiCloudAPIResponseException,
)
from pathlib import Path
import pandas as pd
import sys

APPLE_ID = "ekrivonogov@inbox.ru"
COOKIE_DIR = Path.home() / ".icloud_cookies"
OUT_FILE = Path(__file__).parent / "icloud_photos_metadata.xlsx"


def safe(obj, name):
    return getattr(obj, name, None)


try:
    print("Connecting to iCloud...")

    api = PyiCloudService(
        APPLE_ID,
        cookie_directory=str(COOKIE_DIR)
    )

    print("Connected. Fetching photos metadata...")

    rows = []

    for photo in api.photos.all:
        versions = safe(photo, "versions") or {}

        rows.append({
            "id": safe(photo, "id"),
            "filename": safe(photo, "filename"),
            "item_type": safe(photo, "item_type"),
            "is_live_photo": safe(photo, "is_live_photo"),
            "size_bytes": safe(photo, "size"),
            "width": (safe(photo, "dimensions") or (None, None))[0],
            "height": (safe(photo, "dimensions") or (None, None))[1],
            "created": safe(photo, "created"),
            "asset_date": safe(photo, "asset_date"),
            "added_date": safe(photo, "added_date"),
            "original_url": versions.get("original", {}).get("url"),
            "medium_url": versions.get("medium", {}).get("url"),
            "thumb_url": versions.get("thumb", {}).get("url"),
        })

    if not rows:
        print("No photos found.")
        sys.exit(0)

    df = pd.DataFrame(rows)
    df.to_excel(OUT_FILE, index=False)

    print(f"Saved: {OUT_FILE}")

except PyiCloudFailedLoginException as e:
    print("\n[ERROR] iCloud login failed.")
    print("Reason: Apple temporarily rejected the login.")
    print("What to do:")
    print("- wait 10–30 minutes")
    print("- run auth script again (with password / 2FA)")
    print("- do NOT retry multiple times in a row")
    print(f"Details: {e}")

except PyiCloudAPIResponseException as e:
    print("\n[ERROR] iCloud API error.")
    print("Apple service returned an error (often temporary).")
    print("What to do:")
    print("- wait and retry later")
    print("- check iCloud.com login in browser")
    print(f"Details: {e}")

except Exception as e:
    print("\n[ERROR] Unexpected error.")
    print("The script stopped due to an unexpected exception.")
    print(f"Details: {type(e).__name__}: {e}")
