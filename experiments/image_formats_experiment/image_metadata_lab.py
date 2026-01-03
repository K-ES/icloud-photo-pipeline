from pathlib import Path
from datetime import datetime
from PIL import Image, ExifTags
import pillow_heif
import requests
import re

# ================= CONFIG =================

INPUT_ROOT = Path(r"p:\!PhotoData\02_Extract")
OUTPUT_ROOT = Path(r"p:\!PhotoData\04_WithLocation")

CAMERA_DIR = OUTPUT_ROOT / "camera"
UNKNOWN_DIR = OUTPUT_ROOT / "unknown"

CAMERA_DIR.mkdir(parents=True, exist_ok=True)
UNKNOWN_DIR.mkdir(parents=True, exist_ok=True)

FORMATS = {".jpg", ".jpeg", ".heic", ".png"}
MAX_W, MAX_H = 1920, 1080
SERIES_SECONDS = 5

pillow_heif.register_heif_opener()
TAGS = ExifTags.TAGS

# ================= HELPERS =================

def safe_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:40]

def get_exif(img):
    try:
        return img.getexif() or {}
    except Exception:
        return {}

def extract_datetime(exif):
    for tag_name in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
        for k, v in exif.items():
            if TAGS.get(k) == tag_name:
                try:
                    return datetime.strptime(v, "%Y:%m:%d %H:%M:%S")
                except Exception:
                    pass
    return None

def normalize_datetime(dt):
    if not dt:
        now = datetime.now()
        return datetime(now.year, now.month, now.day, 0, 0, 0)
    return dt

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

def reverse_geocode(gps):
    if not gps:
        return "unknown_place"

    lat, lon = gps
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "jsonv2",
                "accept-language": "ru"
            },
            headers={"User-Agent": "photo-sorter"},
            timeout=10
        )
        data = r.json()
    except Exception:
        return "unknown_place"

    name = data.get("name")
    addr = data.get("address", {})
    city = addr.get("city") or addr.get("town") or addr.get("village")

    if name and city:
        return f"{name}_{city}"
    return name or city or "unknown_place"

def has_gps(exif):
    return any(TAGS.get(k) == "GPSInfo" for k in exif)

def is_screenshot(w, h):
    r = max(w, h) / min(w, h)
    return 2.1 <= r <= 2.8

def is_messenger(exif):
    for k, v in exif.items():
        if TAGS.get(k) == "Software":
            s = str(v).lower()
            return "telegram" in s or "whatsapp" in s
    return False

def is_camera(exif, w, h):
    make = str(exif.get(271, "")).lower()
    model = str(exif.get(272, "")).lower()
    r = max(w, h) / min(w, h)
    return "apple" in make and "iphone" in model and 1.2 <= r <= 1.4

def resize_fhd(img):
    img.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
    return img

def size_tag(w, h):
    return f"{w:04d}x{h:04d}"

# ================= PREPASS: SERIES =================

files = [
    f for f in INPUT_ROOT.rglob("*")
    if f.suffix.lower() in FORMATS
]

records = []

for f in files:
    try:
        with Image.open(f) as img:
            exif = get_exif(img)
            dt = normalize_datetime(extract_datetime(exif))
            records.append((f, dt))
    except Exception:
        continue

records.sort(key=lambda x: x[1])

series_flags = {}
current = []

for f, dt in records:
    if not current:
        current = [(f, dt)]
        continue

    _, prev_dt = current[-1]
    if abs((dt - prev_dt).total_seconds()) <= SERIES_SECONDS:
        current.append((f, dt))
    else:
        if len(current) > 1:
            for x, _ in current:
                series_flags[x] = True
        current = [(f, dt)]

if len(current) > 1:
    for x, _ in current:
        series_flags[x] = True

# ================= MAIN =================

global_index = 1

for f, dt in records:
    try:
        with Image.open(f) as img:
            exif = get_exif(img)
            w, h = img.size

            dt_str = dt.strftime("%Y_%m_%d_%H_%M_%S")
            gps = extract_gps(exif)
            location = safe_slug(reverse_geocode(gps))

            num_part = f"{global_index:03d}"
            series_part = "XXXXXXXXXXXXXXXXXXX" if series_flags.get(f, False) else None

            if is_camera(exif, w, h):
                out_dir = CAMERA_DIR
                parts = [dt_str, location, num_part]
                if series_part:
                    parts.append(series_part)
                name = "__".join(parts) + ".jpg"
            else:
                out_dir = UNKNOWN_DIR
                reason = (
                    "vozmozhno_screenshot"
                    if is_screenshot(w, h)
                    else "vozmozhno_iz_chatov"
                )
                parts = [
                    dt_str,
                    location,
                    size_tag(w, h),
                    num_part
                ]
                if series_part:
                    parts.append(series_part)
                parts.append(reason)
                name = "__".join(parts) + ".jpg"

            img = resize_fhd(img)
            img.convert("RGB").save(out_dir / name, "JPEG", quality=92)

            print("saved:", name)
            global_index += 1

    except Exception as e:
        print("skip:", f.name, e)
