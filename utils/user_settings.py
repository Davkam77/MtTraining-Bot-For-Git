import json
import os

SETTINGS_FILE = os.path.join("data", "user_settings.json")

def load_settings():
    path = 'data/user_settings.json'
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return {}  # если файла нет или он пустой — вернуть пустой словарь

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_user_plan(user_id: int) -> tuple[str, int]:
    settings = load_settings()
    plan_string = settings.get(str(user_id), "1_month|30")  # по умолчанию
    if "|" in plan_string:
        plan, duration = plan_string.split("|")
        return plan, int(duration)
    return plan_string, 30
