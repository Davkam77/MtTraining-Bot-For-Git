# utils/workout_logic.py

from utils.database import (
    get_user_profile,
    save_workout_settings,
    save_mealplan,
    save_daily_workout,
)
from utils.meal_api import get_meal_plan
from utils.workout_loader import generate_workout
from datetime import datetime

def auto_generate_after_metrics(user_id: int) -> str:
    profile = get_user_profile(user_id)
    if not profile:
        return "⚠️ Не удалось найти профиль пользователя."

    weight = profile["weight"]
    height = profile["height"]
    age = profile["age"]

    # Примерная цель – минус 8% веса
    goal_loss = round(weight * 0.08, 1)
    goal_weight = round(weight - goal_loss, 1)

    # Безопасный план: 3 месяца по 45 минут
    months = 3
    duration = 45

    # Сохраняем настройки
    save_workout_settings(user_id, duration_minutes=duration, months=months)

    # Генерируем рацион
    today = datetime.now().strftime("%Y-%m-%d")
    meal = get_meal_plan()
    save_mealplan(user_id, today, meal)

    # Генерируем тренировку
    workout = generate_workout(user_id)
    save_daily_workout(user_id, today, workout)

    # Возвращаем результат
    return (
        f"🎯 Цель: сбросить {goal_loss} кг (до {goal_weight} кг)\n"
        f"📅 План: {months} месяца, по {duration} минут в день\n\n"
        f"🍽️ <b>Меню на сегодня:</b>\n{meal}\n\n"
        f"💪 <b>Тренировка на сегодня:</b>\n{workout}\n\n"
        f"⏰ Хочешь получать это каждый день автоматически? Нажми /wake и задай удобное время."
    )
