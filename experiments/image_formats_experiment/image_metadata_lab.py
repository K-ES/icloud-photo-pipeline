from pathlib import Path
from datetime import datetime
from PIL import Image, ExifTags, ImageDraw, ImageFont
import pillow_heif
import requests
import re
import shutil

# ================= CONFIG =================

INPUT_ROOT = Path(r"p:\!PhotoData\02_Extract")
OUTPUT_ROOT = Path(r"p:\!PhotoData\04_WithLocation")

RUN_DATE = datetime.now().strftime("%Y_%m_%d")

CAMERA_DIR = OUTPUT_ROOT / f"camera_{RUN_DATE}"
UNKNOWN_DIR = OUTPUT_ROOT / f"unknown_{RUN_DATE}"

FORMATS = {".jpg", ".jpeg", ".heic", ".png"}
MAX_W, MAX_H = 1920, 1080
SERIES_SECONDS = 5

FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"

pillow_heif.register_heif_opener()
TAGS = ExifTags.TAGS

# ================= PREPARE OUTPUT =================

if OUTPUT_ROOT.exists():
    for p in OUTPUT_ROOT.iterdir():
        if p.is_dir():
            shutil.rmtree(p)

CAMERA_DIR.mkdir(parents=True, exist_ok=True)
UNKNOWN_DIR.mkdir(parents=True, exist_ok=True)

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
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": gps[0],
                "lon": gps[1],
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

def resize_fhd(img):
    img.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
    return img

def size_tag(w, h):
    return f"{w}x{h}"

def is_camera_file(path: Path) -> bool:
    if path.suffix.lower() == ".png":
        return False
    return re.match(r"img_\d+", path.stem.lower()) is not None

def draw_caption(img, dt: datetime, location: str):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(FONT_PATH), 32)

    line1 = dt.strftime("%Y-%m-%d %H:%M:%S")
    line2 = location.replace("_", " ")

    pad = 16
    lh = font.size + 6

    w1 = draw.textlength(line1, font)
    w2 = draw.textlength(line2, font)
    box_w = int(max(w1, w2)) + pad * 2
    box_h = lh * 2 + pad * 2

    x = pad
    y = img.height - box_h - pad

    draw.rectangle(
        [x, y, x + box_w, y + box_h],
        fill=(0, 0, 0)
    )

    draw.text((x + pad, y + pad), line1, fill="white", font=font)
    draw.text((x + pad, y + pad + lh), line2, fill="white", font=font)

    return img

# ================= PREPASS: SERIES =================

files = [f for f in INPUT_ROOT.rglob("*") if f.suffix.lower() in FORMATS]

records = []
for f in files:
    try:
        with Image.open(f) as img:
            dt = normalize_datetime(extract_datetime(get_exif(img)))
            records.append((f, dt))
    except Exception:
        pass

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
            w, h = img.size

            dt_str = dt.strftime("%Y_%m_%d_%H_%M_%S")
            orig_name = safe_slug(f.stem)

            gps = extract_gps(get_exif(img))
            location = safe_slug(reverse_geocode(gps))

            num_part = f"{global_index:03d}"
            series_part = "XXXXXXXXXXXXXXXXXXX" if series_flags.get(f) else None

            # ===== CAMERA =====
            if is_camera_file(f):
                out_dir = CAMERA_DIR
                parts = [location, num_part]
                if series_part:
                    parts.append(series_part)

                img = resize_fhd(img)
                img = img.convert("RGB")
                img = draw_caption(img, dt, location)

                name = "__".join([dt_str, orig_name, *parts]) + ".jpg"
                img.save(out_dir / name, "JPEG", quality=92)

            # ===== UNKNOWN =====
            else:
                out_dir = UNKNOWN_DIR
                parts = [location, size_tag(w, h), num_part]
                if series_part:
                    parts.append(series_part)

                img = img.convert("RGB")
                img = draw_caption(img, dt, location)

                name = "__".join([dt_str, orig_name, *parts]) + f.suffix.lower()
                img.save(out_dir / name)

            print(f"saved ({out_dir}): {name}")
            global_index += 1

    except Exception as e:
        print("skip:", f.name, e)
