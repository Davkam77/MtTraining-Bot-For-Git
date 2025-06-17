import json
import os
import random
import logging
from utils.user_settings import get_user_plan

WORKOUT_PATH = os.path.join("data", "workouts.json")


def load_workout(user_id: int):
    plan_length = get_user_plan(user_id)
    file_path = os.path.join("data", "workouts.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        all_workouts = data.get(plan_length)
        if not all_workouts:
            return f"❗ Нет тренировок для плана {plan_length}."

        # ⏱ Получаем нужную длительность из строки плана
        duration = None
        if "," in plan_length:
            _, time_part = plan_length.split(",", 1)
            duration = time_part.strip()

        # 🔍 Фильтруем по длительности
        filtered = [w for w in all_workouts if w.get("duration") == duration]
        if not filtered:
            return f"⚠️ Нет тренировок на {duration} для плана {plan_length}"

        workout = random.choice(filtered)
        exercises = "\n".join([f"• {ex}" for ex in workout["exercises"]])
        return f"<b>🏋️ {workout['name']}</b>\n⏱ {workout['duration']}\n\n{exercises}"

    except Exception as e:
        return f"❗ Ошибка загрузки: {str(e)}"



def generate_workout() -> str:
    try:
        with open(WORKOUT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        all_workouts = []
        for plan in data.values():
            all_workouts.extend(plan)

        if not all_workouts:
            return "⚠️ Нет доступных тренировок."

        workout = random.choice(all_workouts)
        exercises = "\n".join([f"• {ex}" for ex in workout.get("exercises", [])])
        return f"<b>🏋️ {workout.get('name', 'Без названия')}</b>\n⏱ {workout.get('duration', 'Не указано')}\n\n{exercises}"

    except Exception as e:
        logging.exception("Ошибка при генерации случайной тренировки:")
        return f"❌ Ошибка загрузки тренировок: {str(e)}"
