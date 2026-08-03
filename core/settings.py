import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "settings.json")
DEFAULTS = {"theme": "light"}


def load_settings():
    settings = dict(DEFAULTS)
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                settings.update(data)
        except (json.JSONDecodeError, OSError):
            pass
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_theme():
    return load_settings().get("theme", "light")


def set_theme(mode):
    settings = load_settings()
    settings["theme"] = mode
    save_settings(settings)
