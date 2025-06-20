# modules/session_manager.py

import os
import json
from datetime import datetime

DATA_DIR = "data"

def list_sessions():
    return sorted(f[:-5] for f in os.listdir(DATA_DIR) if f.endswith(".json"))

def load_session(session_id):
    path = os.path.join(DATA_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_session(session_id, messages):
    path = os.path.join(DATA_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def new_session_id():
    return datetime.now().strftime("session_%Y%m%d_%H%M%S")
