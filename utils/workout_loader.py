import json
import os
import random
from utils.user_settings import get_user_plan

def load_workout(user_id: int):
    plan_length, duration = get_user_plan(user_id)
    filename = f"workouts{duration}.json"
    file_path = os.path.join("data", filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        duration_key = f"{duration}_minutes"
        workouts = data.get(duration_key, {}).get(plan_length)

        if not workouts:
            return f"❗ Нет тренировок для плана {plan_length} и {duration} минут."

        workout = random.choice(workouts)
        exercises = "\n".join([f"• {ex}" for ex in workout["exercises"]])
        return f"<b>🏋️ {workout['name']}</b>\n⏱ {workout['duration']}\n\n{exercises}"

    except FileNotFoundError:
        return f"❌ Файл с тренировками на {duration} минут не найден."
    except Exception as e:
        return f"❌ Ошибка загрузки тренировок: {e}"


def generate_workout(user_id: int) -> str:
    try:
        plan, duration = get_user_plan(user_id)  # Например: "1_month", 45
        file_path = os.path.join("data", f"workouts{duration}.json")

        if not os.path.exists(file_path):
            return f"❌ Файл {file_path} не найден."

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        duration_key = f"{duration}_minutes"
        plan_data = data.get(duration_key, {}).get(plan)

        if not plan_data:
            return f"❗ Нет тренировок для плана {plan} и {duration} минут."

        workout = random.choice(plan_data)
        exercises = "\n".join([f"• {ex}" for ex in workout["exercises"]])
        return f"<b>🏋️ {workout['name']}</b>\n⏱ {workout['duration']}\n\n{exercises}"

    except Exception as e:
        return f"❌ Ошибка генерации тренировок: {e}"
