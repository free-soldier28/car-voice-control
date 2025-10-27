import os
import json
import logging
from settings import load_settings
from vosk_stream import run_vosk_stream

# === Configuration ===
MODEL_RU_PATH = "vosk-model-small-ru-0.22"
MODEL_EN_PATH = "vosk-model-small-en-us-0.15"
COMMANDS_FILE = "commands.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_commands():
    """Load commands from JSON."""
    if not os.path.exists(COMMANDS_FILE):
        logging.error(f"❌ Commands file not found: {COMMANDS_FILE}")
        return {}

    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    try:
        lang = load_settings()
        logging.info(f"🌐 Language set to: {lang}")

        commands = load_commands()
        if not commands:
            logging.error("❌ No commands loaded. Exiting.")
            return

        model_path = MODEL_RU_PATH if lang == "RU" else MODEL_EN_PATH
        run_vosk_stream(lang, commands, model_path)
    except KeyboardInterrupt:
        print("\n🛑 Stopping recognition...")
    except Exception as e:
        logging.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
