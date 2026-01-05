import os
import sys
from pathlib import Path

REQUIRED_ENV_VARS = [
    "PHOTO_OPT_INPUT_DIR",
    "PHOTO_OPT_OUTPUT_DIR",
]

def require_env(vars_):
    missing = [v for v in vars_ if not os.getenv(v)]
    if missing:
        print("ERROR: required environment variables are missing:", file=sys.stderr)
        for v in missing:
            print(f" - {v}", file=sys.stderr)
        sys.exit(1)

require_env(REQUIRED_ENV_VARS)

INPUT_DIR = Path(os.environ["PHOTO_OPT_INPUT_DIR"])
OUTPUT_DIR = Path(os.environ["PHOTO_OPT_OUTPUT_DIR"])

if not INPUT_DIR.exists():
    print(f"ERROR: input dir does not exist: {INPUT_DIR}", file=sys.stderr)
    sys.exit(2)

if not OUTPUT_DIR.exists():
    print(f"ERROR: output dir does not exist: {OUTPUT_DIR}", file=sys.stderr)
    sys.exit(3)
