import os
import json
import logging

SETTINGS_FILE = "settings.json"

def load_settings():
    """Load language setting from settings.json."""
    if not os.path.exists(SETTINGS_FILE):
        logging.error(f"❌ Settings file not found: {SETTINGS_FILE}")
        return "EN"
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        lang = data.get("language", "EN").upper()
        if lang not in ("RU", "EN"):
            logging.warning("⚠️ Invalid language in settings.json. Using EN.")
            return "EN"
        return lang
