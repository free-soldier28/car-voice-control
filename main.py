import os
import json
import logging
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# === Configuration ===
MODEL_RU_PATH = "vosk-model-small-ru-0.22"
MODEL_EN_PATH = "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
CHANNELS = 1
WORDS_PER_LINE = 10
SETTINGS_FILE = "settings.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_settings():
    """Load language setting from settings.json."""
    if not os.path.exists(SETTINGS_FILE):
        logging.error(f"❌ Settings file not found: {SETTINGS_FILE}")
        return "EN"  # default
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        lang = data.get("language", "EN").upper()
        if lang not in ("RU", "EN"):
            logging.warning("⚠️ Invalid language in settings.json. Using EN.")
            return "EN"
        return lang


def print_wrapped(text, lang):
    """Print text 10 words per line."""
    words = text.split()
    for i in range(0, len(words), WORDS_PER_LINE):
        print(f"\n🗣️ [{lang}] {' '.join(words[i:i + WORDS_PER_LINE])}")


def run_vosk_stream(lang):
    """Run real-time recognition using language from settings.json."""
    model_path = MODEL_RU_PATH if lang == "RU" else MODEL_EN_PATH

    if not os.path.exists(model_path):
        logging.error(f"❌ Model not found: {model_path}")
        return

    logging.info(f"Loading {lang} model (this may take a while)...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    logging.info("✅ Model loaded successfully.")

    # Используем микрофон по умолчанию
    device_index = sd.default.device[0]
    device_info = sd.query_devices(device_index)
    logging.info(f"🎧 Capturing from default microphone: {device_info['name']} @ {SAMPLE_RATE} Hz")
    logging.info("🎤 Listening... Press Ctrl+C to stop.\n")

    partial_text = ""

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        device=device_index,
        dtype="int16",
        channels=CHANNELS,
    ) as stream:
        while True:
            data, overflowed = stream.read(4000)
            if overflowed:
                logging.warning("⚠️ Audio buffer overflow detected!")

            data_bytes = bytes(data)

            if recognizer.AcceptWaveform(data_bytes):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    print_wrapped(text, lang)
                partial_text = ""
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "").strip()
                if partial and partial != partial_text:
                    partial_text = partial
                    print(f"\r... [{lang}] {partial_text}", end="", flush=True)


def main():
    try:
        lang = load_settings()
        logging.info(f"🌐 Language set to: {lang}")
        run_vosk_stream(lang)
    except KeyboardInterrupt:
        print("\n🛑 Stopping recognition...")
    except Exception as e:
        logging.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
