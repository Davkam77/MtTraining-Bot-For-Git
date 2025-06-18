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
    user_id = str(user_id)

    if isinstance(settings.get(user_id), dict):
        settings[user_id]["plan"] = f"{plan}|{duration}"
    else:
        settings[user_id] = {
            "plan": f"{plan}|{duration}"
        }

    save_settings(settings)

def get_user_plan(user_id: int) -> tuple[str, int]:
    settings = load_settings()
    user_id = str(user_id)
    plan_data = settings.get(user_id)

    if isinstance(plan_data, dict):
        plan_string = plan_data.get("plan", "1_month|30")
    else:
        plan_string = plan_data or "1_month|30"

    if "|" in plan_string:
        plan, duration = plan_string.split("|")
        return plan, int(duration)
    return plan_string, 30

def set_wake_time(user_id: int, time: str):
    settings = load_settings()
    user_id = str(user_id)

    if isinstance(settings.get(user_id), dict):
        settings[user_id]["wake_time"] = time
    else:
        settings[user_id] = {
            "plan": "1_month|30",  # по умолчанию, если не было
            "wake_time": time
        }

    save_settings(settings)

def get_wake_time(user_id: int) -> str:
    settings = load_settings()
    user_id = str(user_id)

    user_data = settings.get(user_id)
    if isinstance(user_data, dict):
        return user_data.get("wake_time", "08:00")
    return "08:00"
