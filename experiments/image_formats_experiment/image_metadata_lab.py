from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pillow_heif
import requests

# ---------- config ----------

INPUT_DIR = Path(r"p:\!PhotoData\02_Extract\heic\Фото iCloud")
OUTPUT_DIR = Path(r"p:\!PhotoData\04_WithLocation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
USER_AGENT = "photo-location-caption"

pillow_heif.register_heif_opener()

# ---------- helpers ----------

def dms_to_deg(dms):
    d, m, s = dms
    return float(d) + float(m) / 60 + float(s) / 3600


def extract_gps(exif):
    gps = exif.get_ifd(0x8825)
    if not gps:
        return None

    lat = dms_to_deg(gps[2])
    if gps.get(1) == "S":
        lat = -lat

    lon = dms_to_deg(gps[4])
    if gps.get(3) == "W":
        lon = -lon

    return lat, lon


def reverse_geocode(lat, lon):
    params = {"format": "jsonv2", "lat": lat, "lon": lon}
    headers = {"User-Agent": USER_AGENT}

    r = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    name = data.get("name")
    address = data.get("address", {})
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("county")
    )
    country = address.get("country")

    if name and city:
        return f"{name} · {city}"
    if city and country:
        return f"{city} · {country}"
    return data.get("display_name")


def get_photo_datetime(img):
    exif = img.getexif()
    dt = exif.get(36867) or exif.get(306)
    if not dt:
        return None
    return datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")


def add_caption(img, place, photo_dt):
    w, h = img.size
    caption_h = int(h * 0.12)

    base = Image.new("RGBA", (w, h + caption_h), (0, 0, 0, 255))
    base.paste(img.convert("RGBA"), (0, 0))
    draw = ImageDraw.Draw(base)

    main_font = ImageFont.truetype(str(FONT_PATH), int(caption_h * 0.30))
    date_font = ImageFont.truetype(str(FONT_PATH), int(caption_h * 0.20))

    overlay = Image.new("RGBA", (w, caption_h), (0, 0, 0, 160))
    base.paste(overlay, (0, h), overlay)

    # place
    tb = draw.textbbox((0, 0), place, font=main_font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]

    text_x = (w - tw) // 2
    text_y = h + int(caption_h * 0.18)

    draw.text((text_x, text_y), place, (255, 255, 255, 255), font=main_font)

    # datetime
    if photo_dt:
        dt_text = photo_dt.strftime("%Y-%m-%d %H:%M")

        db = draw.textbbox((0, 0), dt_text, font=date_font)
        dt_w, dt_h = db[2] - db[0], db[3] - db[1]

        dt_x = (w - dt_w) // 2
        dt_y = text_y + th + 4

        draw.text((dt_x, dt_y), dt_text, (200, 200, 200, 220), font=date_font)

    return base.convert("RGB")


# ---------- main ----------

def process_file(path: Path):
    try:
        with Image.open(path) as img:
            exif = img.getexif()
            if not exif:
                return

            gps = extract_gps(exif)
            if not gps:
                return

            lat, lon = gps
            place = reverse_geocode(lat, lon)
            photo_dt = get_photo_datetime(img)

            out_img = add_caption(img, place, photo_dt)
            out_path = OUTPUT_DIR / f"{path.stem}_location.jpg"
            out_img.save(out_path, quality=95)

    except Exception as e:
        print(f"ERROR {path}: {e}")


def main():
    for f in INPUT_DIR.rglob("*"):
        if f.suffix.lower() in {".heic", ".jpg", ".jpeg"}:
            process_file(f)


if __name__ == "__main__":
    main()
