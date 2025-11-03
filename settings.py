import os
import json
import logging

def load_settings(file_path):
    """Load language, activation flag, activation words, and timeout from settings.json."""
    if not os.path.exists(file_path):
        logging.error(f"❌ Settings file not found: {file_path}")
        return "EN", True, [], 5

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lang = data.get("language", "EN").upper()
    if lang not in ("RU", "EN"):
        logging.warning("⚠️ Invalid language in settings.json. Using EN.")
        lang = "EN"

    use_activation = data.get("use_activation", True)
    if not isinstance(use_activation, bool):
        logging.warning("⚠️ use_activation must be true or false. Using True.")
        use_activation = True

    activation_words = data.get("activation_words", [])
    if not isinstance(activation_words, list):
        logging.warning("⚠️ activation_words must be a list. Using empty list.")
        activation_words = []

    timeout = data.get("activation_timeout", 5)
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        logging.warning("⚠️ activation_timeout must be a positive number. Using default 5.")
        timeout = 5

    return lang, use_activation, activation_words, timeout
