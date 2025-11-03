import difflib
import os
import re
import logging
import json

from utils.output import print_wrapped

def handle_command(text: str, commands: dict, lang: str):
    match = match_exact(text, commands)
    if match:
        print_wrapped(f"✅ Command recognized: {text} → {match}", lang)
        return

    fuzzy = match_fuzzy(text, commands)
    if fuzzy:
        matched_key, response, confidence = fuzzy
        print_wrapped(f"✅ Command recognized: {text} → {response}", lang)
        logging.debug(f"🤖 Fuzzy match: '{text}' ≈ '{matched_key}' (confidence: {confidence:.2f})")
        return

    print_wrapped(f"❌ Unrecognized: {text}", lang)

def match_exact(text: str, commands: dict) -> str | None:
    for cmd_pattern, response in commands.items():
        pattern = re.sub(r"\{.*?\}", r"(.+)", cmd_pattern)
        match = re.fullmatch(pattern, text)
        if match:
            return response.format(*match.groups(), value=match.group(1)) if match.groups() else response
    return None

def match_fuzzy(text: str, commands: dict, cutoff: float = 0.85) -> tuple[str, str, float] | None:
    candidates = list(commands.keys())
    closest = difflib.get_close_matches(text, candidates, n=1, cutoff=cutoff)
    if not closest:
        return None

    matched_key = closest[0]
    confidence = difflib.SequenceMatcher(None, text, matched_key).ratio()
    response = commands[matched_key]
    return matched_key, response, confidence

def load_commands(file_path: str):
    """Load commands from JSON."""
    if not os.path.exists(file_path):
        logging.error(f"❌ Commands file not found: {file_path}")
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
