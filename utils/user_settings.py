import json
import os

SETTINGS_FILE = os.path.join("data", "user_settings.json")

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def set_user_plan(user_id: int, plan: str):
    settings = load_settings()
    settings[str(user_id)] = plan
    save_settings(settings)

def get_user_plan(user_id: int) -> str:
    settings = load_settings()
    return settings.get(str(user_id), "1_month")  # default
