import os
import json
import logging
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from settings import load_settings  # import settings module

# === Configuration ===
MODEL_RU_PATH = "vosk-model-small-ru-0.22"
MODEL_EN_PATH = "vosk-model-small-en-us-0.15"
CHANNELS = 1
WORDS_PER_LINE = 10
SETTINGS_FILE = "settings.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def print_wrapped(text, lang):
    """Print text with a maximum of WORDS_PER_LINE words per line."""
    words = text.split()
    for i in range(0, len(words), WORDS_PER_LINE):
        print(f"\n🗣️ [{lang}] {' '.join(words[i:i + WORDS_PER_LINE])}")


def run_vosk_stream(lang):
    """Run real-time speech recognition using the selected language."""
    # Select model and correct sample rate
    if lang == "RU":
        model_path = MODEL_RU_PATH
    else:
        model_path = MODEL_EN_PATH

    sample_rate = 16000  # small models expect 16 kHz

    if not os.path.exists(model_path):
        logging.error(f"❌ Model not found: {model_path}")
        return

    logging.info(f"Loading {lang} model (this may take a while)...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)
    logging.info("✅ Model loaded successfully.")

    # Always use default microphone
    device_index = sd.default.device[0]
    device_info = sd.query_devices(device_index)
    logging.info(f"🎧 Capturing from default microphone: {device_info['name']} @ {sample_rate} Hz")
    logging.info("🎤 Listening... Press Ctrl+C to stop.\n")

    # Start capturing audio
    with sd.RawInputStream(
        samplerate=sample_rate,
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

            # Process the waveform
            if recognizer.AcceptWaveform(data_bytes):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    print_wrapped(text, lang)


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
