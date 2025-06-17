import json
import os
import random
from utils.user_settings import get_user_plan

def load_workout(user_id: int):
    plan_length = get_user_plan(user_id)
    file_path = os.path.join("data", "workouts.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        workouts = data.get(plan_length)
        if not workouts:
            return f"❗ Нет тренировок для плана {plan_length}."

        workout = random.choice(workouts)
        exercises = "\n".join([f"• {ex}" for ex in workout["exercises"]])
        return f"<b>🏋️ {workout['name']}</b>\n⏱ {workout['duration']}\n\n{exercises}"

    except Exception as e:
        return f"❗ Ошибка загрузки: {str(e)}"

def generate_workout():
    workout_path = os.path.join("data", "workout.json")
    try:
        with open(workout_path, "r", encoding="utf-8") as f:
            workouts = json.load(f)
            if not workouts:
                return "⚠️ Нет доступных тренировок."
            return random.choice(workouts)
    except Exception as e:
        return f"❌ Ошибка загрузки тренировок: {e}"
