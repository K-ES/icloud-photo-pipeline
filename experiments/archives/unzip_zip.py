import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)

log("PROGRAM START")

# ENV
log("Reading environment variables")
input_dir = os.getenv("PHOTO_OPT_INPUT_DIR")
output_dir = os.getenv("PHOTO_OPT_OUTPUT_DIR")

log(f"PHOTO_OPT_INPUT_DIR = {input_dir}")
log(f"PHOTO_OPT_OUTPUT_DIR = {output_dir}")

if not input_dir or not output_dir:
    log("Missing required environment variables", level="ERROR")
    sys.exit(1)

# Paths
input_path = Path(input_dir)
output_path = Path(output_dir)

log(f"Resolved input path: {input_path}")
log(f"Resolved output path: {output_path}")

if not input_path.exists():
    log(f"Input directory does not exist: {input_path}", level="ERROR")
    sys.exit(1)

if not output_path.exists():
    log(f"Output directory does not exist, creating: {output_path}")
    output_path.mkdir(parents=True, exist_ok=True)

# Scan input
log("Scanning input directory for zip files")
all_files = list(input_path.iterdir())
log(f"Total entries in input dir: {len(all_files)}")

zip_files = [p for p in all_files if p.is_file() and p.suffix.lower() == ".zip"]
log(f"ZIP files found: {len(zip_files)}")

# Unzip loop
for idx, zip_file in enumerate(zip_files, start=1):
    log(f"[{idx}/{len(zip_files)}] Processing zip: {zip_file.name}")
    try:
        with zipfile.ZipFile(zip_file, "r") as z:
            names = z.namelist()
            log(f"{zip_file.name}: contains {len(names)} entries")
            for n in names:
                log(f"{zip_file.name}: entry -> {n}")
            z.extractall(output_path)
        log(f"{zip_file.name}: extracted successfully")
    except Exception as e:
        log(f"Failed to extract {zip_file.name}: {e}", level="ERROR")
        sys.exit(1)

# Final stats
log("Scanning output directory after extraction")
out_files = list(output_path.rglob("*"))
log(f"Total entries in output dir: {len(out_files)}")

files_only = [p for p in out_files if p.is_file()]
log(f"Total files in output dir: {len(files_only)}")

log("PROGRAM END")
