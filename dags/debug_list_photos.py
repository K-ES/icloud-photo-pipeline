from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException
from datetime import datetime
from pathlib import Path
import logging

BASE_DIR = Path("/mnt/p/airflow_media_inbox")
REQUIRED_FILES = [
    "Фото iCloud jpeg.zip",
    "Фото iCloud heic.zip",
]

def inspect_inbox():
    log = logging.getLogger("airflow.task")

    log.info("📂 checking inbox directory")

    if not BASE_DIR.exists():
        log.error("❌ inbox directory does not exist")
        raise AirflowException(f"Inbox directory does not exist: {BASE_DIR}")

    if not BASE_DIR.is_dir():
        log.error("❌ inbox path is not a directory")
        raise AirflowException(f"Inbox path is not a directory: {BASE_DIR}")

    log.info(f"✅ inbox directory OK: {BASE_DIR}")

    for fname in REQUIRED_FILES:
        f = BASE_DIR / fname

        if not f.exists():
            log.error(f"❌ required file missing: {f.name}")
            raise AirflowException(f"Required file is missing: {f}")

        size_mb = f.stat().st_size / 1024 / 1024
        log.info(f"📦 file found | {f.name} | {size_mb:.2f} MB")
        log.info("😀 😁 😂 🤣 😃 😄 😅 😆 😉 😊 😋 😎 😍 😘 😗 😙 😚 🙂 🤗 🤩 🤔 🤨 😐 😑 😶 🙄 😏 😣 😥 😮 🤐 😯 😪 😫 😴")
        log.info("😌 😛 😜 😝 🤤 😒 😓 😔 😕 🙃 🤑 😲 ☹️ 🙁 😖 😞 😟 😤 😢 😭 😦 😧 😨 😩 🤯 😬 😰 😱 🥵 🥶 😳 🤪 😵 😡 😠 🤬")
        log.info("🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵 🙈 🙉 🙊 🐔 🐧 🐦 🐤 🐣 🐥 🦆 🦅 🦉 🦇 🐺 🐗 🐴 🦄 🐝 🐛 🦋 🐌 🐞")
        log.info("🌵 🌲 🌳 🌴 🌱 🌿 ☘️ 🍀 🎍 🎋 🍃 🍂 🍁 🍄 🌾 💐 🌷 🌹 🌺 🌸 🌼 🌻 🌞 🌝 🌛 🌜 🌚 🌕 🌖 🌗 🌘 🌑 🌒 🌓 🌔 🌙 ⭐ 🌟 ✨")
        log.info("🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🫐 🍈 🍒 🍑 🥭 🍍 🥥 🥝 🍅 🍆 🥑 🥦 🥬 🥒 🌶️ 🫑 🌽 🥕 🫒 🧄 🧅 🥔 🍠 🥐 🥯 🍞 🧀 🥚 🍳")
        log.info("🍔 🍟 🍕 🌭 🥪 🌮 🌯 🫔 🥗 🥘 🍝 🍜 🍲 🍛 🍣 🍱 🍤 🍙 🍚 🍘 🍥 🥮 🍢 🍡 🍧 🍨 🍦 🥧 🧁 🍰 🎂 🍮 🍭 🍬 🍫 🍿 🍩 🍪")
        log.info("⚙️ 🔧 🔨 🛠️ ⛏️ 🔩 ⚡ 🔥 💡 🔌 🖥️ 💻 🖨️ 🖱️ ⌨️ 📱 📲 📞 📡 🌐 🛰️ 💾 💿 📀 🧮 🧠 🤖 🧪 🧫 🧬 🔬 🔭 📊 📈 📉 📂 📁 🗂️")
        log.info("🚗 🚕 🚙 🚌 🚎 🏎️ 🚓 🚑 🚒 🚐 🚚 🚛 🚜 🏍️ 🛵 🚲 🛴 🚨 🚥 🚦 🛑 ✈️ 🛫 🛬 🚀 🛰️ 🚁 🚤 ⛴️ 🚢 ⚓ 🗺️ 🧭 ⏰ ⏱️ ⏲️ ⏳ ⌛")
        log.info("✔️ ❌ ⚠️ ❗ ❓ ❕ 🔴 🟡 🟢 🔵 ⚫ ⚪ 🟣 🟤 🔺 🔻 🔹 🔸 🔶 🔷 ♻️ ✅ ☑️ 🔁 🔂 🔄 ⏩ ⏪ ⏫ ⏬ ▶️ ⏸️ ⏹️ ⏺️ 🔊 🔉 🔈 🔇")
        log.info("🎉 inbox inspection finished successfully")

with DAG(
    dag_id="debug_airflow_media_inbox",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    PythonOperator(
        task_id="inspect_media_inbox",
        python_callable=inspect_inbox,
    )
