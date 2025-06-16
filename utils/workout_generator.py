import random
from datetime import datetime
from utils.database import get_workout_settings, save_daily_workout

EXERCISES = {
    "разминка": [
        "Прыжки на месте — 1 мин",
        "Круги руками — 2×30 сек",
        "Наклоны вперёд — 10 раз",
        "Повороты корпуса — 20 раз",
        "Ходьба с высоко поднятыми коленями — 1 мин"
    ],
    "силовые": [
        "Приседания — 3×15",
        "Отжимания — 2×12",
        "Планка — 2×30 сек",
        "Подъёмы таза лёжа — 3×20",
        "Выпады — 2×12 на каждую ногу"
    ],
    "кардио": [
        "Бег на месте — 3×1 мин",
        "Берпи — 3×10",
        "Скалолаз — 3×30 сек",
        "Прыжки звёздочка — 3×15",
        "Прыжки через воображаемую скакалку — 2×1 мин"
    ]
}

def generate_daily_workout(user_id, overwrite=True):
    settings = get_workout_settings(user_id)
    if not settings:
        return "❗ Сначала задай план через /setworkout"

    start_date = datetime.strptime(settings["start_date"], "%Y-%m-%d")
    today = datetime.now()
    days_passed = (today - start_date).days + 1
    total_days = settings["months"] * 30
    duration = settings["duration_minutes"]

    if days_passed > total_days:
        return "🎉 Поздравляем! Ты завершил свой тренировочный план."

    # Генерируем случайные упражнения
    warmup = random.sample(EXERCISES["разминка"], 2)
    strength = random.sample(EXERCISES["силовые"], 2)
    cardio = random.sample(EXERCISES["кардио"], 2)

    workout_text = (
        f"📆 День {days_passed} из {total_days}\n"
        f"🕒 {duration} мин тренировка\n\n"
        f"<b>🔸 Разминка:</b>\n" +
        "\n".join([f"• {w}" for w in warmup]) + "\n\n" +
        f"<b>🔸 Силовые:</b>\n" +
        "\n".join([f"• {s}" for s in strength]) + "\n\n" +
        f"<b>🔸 Кардио:</b>\n" +
        "\n".join([f"• {c}" for c in cardio])
    )

    if overwrite:
        today_str = today.strftime("%Y-%m-%d")
        save_daily_workout(user_id, today_str, workout_text)

    return workout_text
