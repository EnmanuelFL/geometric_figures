import json
import os
import uuid
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "history.json")
MAX_ENTRIES = 20


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data[:MAX_ENTRIES]
    except (json.JSONDecodeError, OSError):
        pass
    return []


def _save(entries):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(entries[:MAX_ENTRIES], f, ensure_ascii=False, indent=2)


def add_entry(figure, parameters, results):
    entry = {
        "id": str(uuid.uuid4())[:8],
        "figure": figure,
        "parameters": parameters,
        "results": results,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    entries = load_history()
    entries.insert(0, entry)
    _save(entries)
    return entry


def delete_entry(entry_id):
    entries = load_history()
    remaining = [e for e in entries if e.get("id") != entry_id]
    _save(remaining)
    return remaining
