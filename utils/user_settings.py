import json
import os

SETTINGS_FILE = os.path.join("data", "user_settings.json")

def load_settings():
    if not os.path.exists(SETTINGS_FILE) or os.path.getsize(SETTINGS_FILE) == 0:
        return {}

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def set_user_plan(user_id: int, plan: str, duration: int):
    settings = load_settings()
    settings[str(user_id)] = f"{plan}|{duration}"
    save_settings(settings)

def get_user_plan(user_id: int) -> tuple[str, int]:
    settings = load_settings()
    plan_string = settings.get(str(user_id), "1_month|30")  # по умолчанию
    if "|" in plan_string:
        plan, duration = plan_string.split("|")
        return plan, int(duration)
    return plan_string, 30
