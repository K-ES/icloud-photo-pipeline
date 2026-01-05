import time
import os
import sys

REQUIRED_ENV_VARS = [
    "PHOTO_OPT_INPUT_DIR",
    "PHOTO_OPT_OUTPUT_DIR",
]

missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]

if missing:
    print("все плохо", file=sys.stderr)
    for v in missing:
        print(f"missing: {v}", file=sys.stderr)
else:
    print("все хорошо")

# держим контейнер живым для осмотра
time.sleep(3600)
