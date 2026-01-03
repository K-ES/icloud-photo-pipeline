# experiments/image_formats_experiment/image_with_location.py

from pathlib import Path
from datetime import datetime
import re
import requests
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont
import pillow_heif

# ================== CONFIG ==================

INPUT_DIR = Path(r"p:\!PhotoData\03_TestFormats")
OUTPUT_DIR = Path(r"p:\!PhotoData\04_WithLocation")

FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"
FONT_SIZE_MAIN = 48     # локация
FONT_SIZE_DATE = 36     # дата

MAX_FILES = 10

pillow_heif.register_heif_opener()

# ================== HELPERS ==================

def safe_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:40]

# ---------- DATE ----------

def extract_datetime(img, exif) -> datetime | None:
    # 1. EXIF (JPEG)
    for tag in (36867, 306):  # DateTimeOriginal, DateTime
        val = exif.get(tag)
        if val:
            try:
                return datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
            except Exception:
                pass

    # 2. XMP (HEIC / iPhone)
    xmp = img.info.get("xmp")
    if xmp:
        try:
            root = ET.fromstring(xmp)
            for el in root.iter():
                if el.tag.endswith("CreateDate"):
                    return datetime.fromisoformat(el.text.replace("Z", ""))
        except Exception:
            pass

    return None

# ---------- GPS ----------

def extract_gps(exif):
    gps = exif.get_ifd(0x8825)
    if not gps:
        return None

    def conv(v):
        return float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600

    lat = conv(gps.get(2))
    if gps.get(1) == "S":
        lat = -lat

    lon = conv(gps.get(4))
    if gps.get(3) == "W":
        lon = -lon

    return lat, lon

# ---------- LOCATION ----------

def reverse_geocode(gps):
    lat, lon = gps
    r = requests.get(
        "https://nominatim.openstreetmap.org/reverse",
        params={
            "lat": lat,
            "lon": lon,
            "format": "jsonv2",
            "accept-language": "ru"
        },
        headers={"User-Agent": "photo-location"},
        timeout=10
    )
    data = r.json()

    name = data.get("name")
    city = data.get("address", {}).get("city") or data.get("address", {}).get("town")

    if name and city:
        return f"{name} · {city}"
    return name or city or "unknown_place"

# ================== IMAGE ==================

def add_caption(img, line1, line2):
    w, h = img.size
    bar_h = int(h * 0.16)

    base = Image.new("RGB", (w, h + bar_h), (0, 0, 0))
    base.paste(img, (0, 0))

    overlay = Image.new("RGBA", (w, bar_h), (0, 0, 0, 160))
    base.paste(overlay, (0, h), overlay)

    draw = ImageDraw.Draw(base)
    font_main = ImageFont.truetype(str(FONT_PATH), FONT_SIZE_MAIN)
    font_date = ImageFont.truetype(str(FONT_PATH), FONT_SIZE_DATE)

    # --- первая строка (локация)
    bbox1 = draw.textbbox((0, 0), line1, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]

    # --- вторая строка (дата)
    bbox2 = draw.textbbox((0, 0), line2, font=font_date)
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]

    y_start = h + (bar_h - h1 - h2 - 10) // 2

    draw.text(
        ((w - w1) // 2, y_start),
        line1,
        fill=(255, 255, 255),
        font=font_main
    )

    draw.text(
        ((w - w2) // 2, y_start + h1 + 10),
        line2,
        fill=(220, 220, 220),
        font=font_date
    )

    return base

# ================== MAIN ==================

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    files = [
        f for f in INPUT_DIR.iterdir()
        if f.suffix.lower() in {".heic", ".jpg", ".jpeg"}
    ][:MAX_FILES]

    for idx, f in enumerate(files, start=1):
        with Image.open(f) as img:
            exif = img.getexif()

            dt = extract_datetime(img, exif)
            dt_part = dt.strftime("%Y_%m_%d_%H_%M_%S") if dt else "unknown_date"
            dt_text = dt.strftime("%d.%m.%Y %H:%M:%S") if dt else "unknown date"

            gps = extract_gps(exif)
            place = reverse_geocode(gps) if gps else "unknown_place"

            out_img = add_caption(img, place, dt_text)

            name = f"{dt_part}__{safe_slug(place)}__{idx}.jpg"
            out_img.save(OUTPUT_DIR / name, quality=95)

            print("saved:", name)

if __name__ == "__main__":
    main()
