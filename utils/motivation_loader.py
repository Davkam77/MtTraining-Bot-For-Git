import json
import os
import random

def get_random_motivation():
    path = os.path.join("data", "motivations.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return random.choice(data) if data else "Будь сильным — ты сможешь всё!"
    except Exception:
        return "🧠 Сегодня отличный день, чтобы сделать шаг вперёд!"
