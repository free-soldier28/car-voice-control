import logging

from settings import load_settings
from engine.vosk_stream import run_vosk_stream
from engine.vosk_config import VoskConfig
from utils.commands import load_commands

# === Configuration ===
MODEL_RU_PATH = "models/vosk-model-small-ru-0.22"
MODEL_EN_PATH = "models/vosk-model-small-en-us-0.15"
COMMANDS_FILE = "commands.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    try:
        lang, use_activation, activation_words, activation_timeout = load_settings()

        logging.info(f"🌐 Language set to: {lang}")
        logging.info(f"🔑 Activation words: {activation_words}")

        commands = load_commands(COMMANDS_FILE)
        if not commands:
            logging.error("❌ No commands loaded. Exiting.")
            return

        model_path = MODEL_RU_PATH if lang == "RU" else MODEL_EN_PATH
        config = VoskConfig(lang, commands, model_path, use_activation, activation_words, activation_timeout)
        run_vosk_stream(config)
    except KeyboardInterrupt:
        print("\n🛑 Stopping recognition...")
    except Exception as e:
        logging.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
