import os
import logging
import time
import json

from vosk import Model, KaldiRecognizer
from engine.vosk_config import VoskConfig
from utils.commands import handle_command
from sound import play_activation, play_deactivation
from utils.output import print_wrapped

def setup_recognizer(config: VoskConfig):
    if not os.path.exists(config.model_path):
        raise FileNotFoundError(f"❌ Model not found: {config.model_path}")

    logging.info(f"📦 Loading {config.lang} model...")
    model = Model(config.model_path)
    recognizer = KaldiRecognizer(model, config.sample_rate)
    recognizer.SetWords(True)
    logging.info("✅ Model loaded successfully.")
    return recognizer

def extract_text(recognizer):
    result_json = json.loads(recognizer.Result())
    return result_json.get("text", "").strip().lower()

def process_text(text: str, config: VoskConfig, state: dict):
    lang = config.lang
    now = time.time()

    if config.use_activation and not state["activated"]:
        if any(word in text for word in state["activation_words"]):
            state["activated"] = True
            state["activation_time"] = now
            print_wrapped(f"🔔 Activation word detected: {text}", lang)
            print_wrapped(f"🕒 Waiting for command (timeout {config.activation_timeout} s)…", lang)
            play_activation()
        return

    if state["activated"]:
        if config.use_activation and now - state["activation_time"] > config.activation_timeout:
            print_wrapped("⏱️ Timeout: No command received.", lang)
            play_deactivation()
            state["activated"] = False
            state["activation_time"] = None
            return

        if text in state["activation_words"]:
            logging.debug("🔁 Ignoring repeated activation word.")
            return

        delay = round(now - state["activation_time"], 2) if state["activation_time"] else 0
        logging.info(f"🧪 Received command: {text}")
        if config.use_activation:
            logging.info(f"⏱️ Delay from activation to command: {delay} seconds")
            print(f"\n🗣️ [{lang}] ⏱️ Delay: {delay} seconds")

        handle_command(text, config.commands, lang)

        if config.use_activation:
            play_deactivation()
            state["activated"] = False
            state["activation_time"] = None
    elif not config.use_activation:
        handle_command(text, config.commands, lang)