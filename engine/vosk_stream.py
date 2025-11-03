import logging
import time

from utils.audio import setup_audio_stream
from engine.vosk_config import VoskConfig
from engine.vosk_core import extract_text, process_text, setup_recognizer

READSIZE = 8000

def init_activation_state(config: VoskConfig):
    return {
        "activated": not config.use_activation,
        "activation_time": time.time() if not config.use_activation else None,
        "activation_words": [w.lower() for w in config.activation_words],
    }

def run_vosk_stream(config: VoskConfig):
    recognizer = setup_recognizer(config)
    stream = setup_audio_stream(config.sample_rate)
    activation_state = init_activation_state(config)

    try:
        with stream:
            logging.info("🎙️ Audio stream started successfully.")
            while True:
                try:
                    data, overflowed = stream.read(READSIZE)
                    if overflowed:
                        logging.warning("⚠️ Audio buffer overflow detected!")

                    if recognizer.AcceptWaveform(bytes(data)):
                        text = extract_text(recognizer)
                        if not text:
                            continue

                        process_text(text, config, activation_state)

                except Exception as e:
                    logging.error(f"⚠️ Recognition error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        logging.error(f"⚠️ Stream setup error: {e}")