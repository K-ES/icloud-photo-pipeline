import time
import logging
import pandas as pd
from tqdm import tqdm
import pyicloud

from pyicloud.exceptions import PyiCloudAPIResponseException
from config import (
    APPLE_ID,
    COOKIE_DIR,
    DOWNLOAD_DIR,
    OUT_EXCEL,
    LOG_FILE
)

# ==============================
# LOG SETUP
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info(f"pyicloud version: {pyicloud.__version__}")

def safe(obj, name):
    return getattr(obj, name, None)

def main():
    start_ts = time.time()

    api = pyicloud.PyiCloudService(
        APPLE_ID,
        cookie_directory=str(COOKIE_DIR)
    )

    photos = list(api.photos.all)
    total = len(photos)
    logging.info(f"Total assets: {total}")

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    rows = []

    for photo in tqdm(photos, desc="Downloading", unit="file"):
        try:
            filename = safe(photo, "filename") or f"{safe(photo,'id')}.bin"
            target = DOWNLOAD_DIR / filename

            if not target.exists():
                data = photo.download()
                with open(target, "wb") as f:
                    f.write(data)

            versions = safe(photo, "versions") or {}

            rows.append({
                "id": safe(photo, "id"),
                "filename": filename,
                "item_type": safe(photo, "item_type"),
                "is_live_photo": safe(photo, "is_live_photo"),
                "size_bytes": safe(photo, "size"),
                "width": (safe(photo, "dimensions") or (None, None))[0],
                "height": (safe(photo, "dimensions") or (None, None))[1],
                "created": safe(photo, "created"),
                "asset_date": safe(photo, "asset_date"),
                "added_date": safe(photo, "added_date"),
                "original_url": versions.get("original", {}).get("url"),
            })

        except PyiCloudAPIResponseException as e:
            logging.error(f"API error asset {safe(photo,'id')}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error asset {safe(photo,'id')}: {e}")

    df = pd.DataFrame(rows)
    df.to_excel(OUT_EXCEL, index=False)

    elapsed = time.time() - start_ts
    logging.info(f"Finished. Time spent: {elapsed:.1f} sec")
    logging.info(f"Excel saved: {OUT_EXCEL}")

if __name__ == "__main__":
    main()
