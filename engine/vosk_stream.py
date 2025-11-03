import os
import json
import logging
import sounddevice as sd
import time

from vosk import Model, KaldiRecognizer
from sound import play_activation, play_deactivation
from utils.output import print_wrapped
from utils.commands import handle_command
from utils.audio import init_audio_device
from engine.vosk_config import VoskConfig

CHANNELS = 1
BLOCKSIZE = 16000
READSIZE = 8000
DTYPE = "int16"

def process_recognition(recognizer, data_bytes):
    if recognizer.AcceptWaveform(data_bytes):
        result_json = json.loads(recognizer.Result())
        text = result_json.get("text", "").strip().lower()
        logging.debug(f"📄 Final result: {text}")
        return text
    else:
        partial_json = json.loads(recognizer.PartialResult())
        partial = partial_json.get("partial", "").strip().lower()
        logging.debug(f"📝 Partial result: {partial}")
        return partial

def run_vosk_stream(config: VoskConfig):
    lang = config.lang
    model_path = config.model_path
    use_activation = config.use_activation
    activation_timeout = config.activation_timeout
    sample_rate = config.sample_rate

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model not found: {model_path}")

    logging.info(f"📦 Loading {lang} model...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)
    logging.info("✅ Model loaded successfully.")

    device_index = init_audio_device(sample_rate)
    logging.info("🎤 Listening... Press Ctrl+C to stop.\n")

    activated = not use_activation  # if activation is off, start in active mode
    activation_time = time.time() if activated else None
    activation_words = [w.lower() for w in config.activation_words]

    try:
        with sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=BLOCKSIZE,
            device=device_index,
            dtype=DTYPE,
            channels=CHANNELS,
        ) as stream:
            logging.info("🎙️ Audio stream started successfully.")
            while True:
                try:
                    data, overflowed = stream.read(READSIZE)
                    if overflowed:
                        logging.warning("⚠️ Audio buffer overflow detected!")

                    text = process_recognition(recognizer, bytes(data))
                    if not text:
                        continue

                    current_time = time.time()

                    if use_activation and not activated:
                        for word in activation_words:
                            if word in text:
                                activated = True
                                activation_time = current_time
                                print_wrapped(f"🔔 Activation word detected: {word}", lang)
                                print_wrapped(f"🕒 Waiting for command (timeout {activation_timeout} s)…", lang)
                                play_activation()
                                break
                        continue

                    if activated:
                        elapsed = current_time - activation_time if activation_time else 0

                        if use_activation and elapsed > activation_timeout:
                            print_wrapped("⏱️ Timeout: No command received.", lang)
                            play_deactivation()
                            activated = False
                            activation_time = None
                            continue

                        if text in activation_words:
                            continue  # skip repeated activation word

                        command_received_time = current_time
                        delay = round(command_received_time - activation_time, 2) if activation_time else 0
                        logging.info(f"🧪 Received command: {text}")
                        if use_activation:
                            logging.info(f"⏱️ Delay from activation to command: {delay} seconds")
                            print(f"\n🗣️ [{lang}] ⏱️ Delay: {delay} seconds")
                        handle_command(text, config.commands, lang)
                        if use_activation:
                            play_deactivation()
                            activated = False
                            activation_time = None

                except Exception as e:
                    logging.error(f"⚠️ Recognition error: {e}")
                    continue

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        logging.error(f"⚠️ Stream setup error: {e}")