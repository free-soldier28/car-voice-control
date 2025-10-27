import os
import json
import logging
import re
import sounddevice as sd
from vosk import Model, KaldiRecognizer

CHANNELS = 1
WORDS_PER_LINE = 10

def print_wrapped(text, lang):
    """Print text with a maximum of WORDS_PER_LINE words per line."""
    words = text.split()
    for i in range(0, len(words), WORDS_PER_LINE):
        print(f"\n🗣️ [{lang}] {' '.join(words[i:i + WORDS_PER_LINE])}")


def handle_command(text, commands, lang):
    """Check recognized text against commands and execute response."""
    for cmd_pattern, response in commands.items():
        # Replace placeholders with regex
        pattern = re.sub(r"\{.*?\}", r"(.+)", cmd_pattern)
        match = re.fullmatch(pattern, text)
        if match:
            # If there are capture groups, replace in response
            if match.groups():
                formatted_response = response.format(*match.groups(), value=match.group(1))
            else:
                formatted_response = response
            print_wrapped(f"✅ Command recognized: {text} -> {formatted_response}", lang)
            return
    # If no command matched
    print_wrapped(f"❌ Unrecognized: {text}", lang)


def run_vosk_stream(lang, commands, model_path, sample_rate=16000):
    """
    Run real-time recognition using the selected language and commands.

    :param lang: 'RU' or 'EN'
    :param commands: dictionary of commands
    :param model_path: path to VOSK model
    :param sample_rate: audio sample rate
    """
    if not os.path.exists(model_path):
        logging.error(f"❌ Model not found: {model_path}")
        return

    logging.info(f"Loading {lang} model...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)  # no grammar to support {value}
    logging.info("✅ Model loaded successfully.")

    # Always use default microphone
    device_index = sd.default.device[0]
    device_info = sd.query_devices(device_index)
    logging.info(f"🎧 Capturing from default microphone: {device_info['name']} @ {sample_rate} Hz")
    logging.info("🎤 Listening... Press Ctrl+C to stop.\n")

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

            if recognizer.AcceptWaveform(data_bytes):
                result_json = json.loads(recognizer.Result())
                text = result_json.get("text", "").strip()
                if text:
                    handle_command(text, commands, lang)
