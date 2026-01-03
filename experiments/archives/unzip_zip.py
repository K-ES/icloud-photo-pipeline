# experiments/archives/unzip_zip.py

from pathlib import Path
import zipfile
import logging

# ===== constants =====
INBOX_DIR = Path(r"p:\!PhotoData\01_Archives")
TARGET_ROOT = Path(r"p:\!PhotoData\02_Extract")

# ===== logging =====
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def extract_all_zips(inbox_dir: Path, target_root: Path) -> None:
    if not inbox_dir.exists():
        raise FileNotFoundError(f"Inbox not found: {inbox_dir}")

    target_root.mkdir(parents=True, exist_ok=True)

    zips = list(inbox_dir.glob("*.zip"))
    logger.info(f"Found {len(zips)} zip archives")

    for archive_path in zips:
        target_dir = target_root / archive_path.stem
        target_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Extracting: {archive_path} -> {target_dir}")

        with zipfile.ZipFile(archive_path, "r") as zf:
            for member in zf.infolist():
                out_path = target_dir / member.filename

                if member.is_dir():
                    out_path.mkdir(parents=True, exist_ok=True)
                    continue

                if out_path.exists():
                    logger.info(f"Skip existing: {out_path}")
                    continue

                out_path.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(out_path, "wb") as dst:
                    dst.write(src.read())

        logger.info(f"Done: {archive_path.name}")


if __name__ == "__main__":
    extract_all_zips(
        inbox_dir=INBOX_DIR,
        target_root=TARGET_ROOT,
    )
