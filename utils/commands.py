import os
import re
import logging
import json

from utils.output import print_wrapped

def handle_command(text, commands, lang):
    for cmd_pattern, response in commands.items():
        pattern = re.sub(r"\{.*?\}", r"(.+)", cmd_pattern)
        logging.debug(f"🔍 Pattern: '{pattern}' | Text: '{text}'")
        match = re.fullmatch(pattern, text)
        if match:
            if match.groups():
                formatted_response = response.format(*match.groups(), value=match.group(1))
            else:
                formatted_response = response
            print_wrapped(f"✅ Command recognized: {text} -> {formatted_response}", lang)
            return
    print_wrapped(f"❌ Unrecognized: {text}", lang)

def load_commands(file_path):
    """Load commands from JSON."""
    if not os.path.exists(file_path):
        logging.error(f"❌ Commands file not found: {file_path}")
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
