def generate_workout(activity_level):
    if activity_level < 1.3:
        return "🏃 Прогулка 30 минут + Растяжка 10 минут"
    elif activity_level < 1.5:
        return "🏋️ 20 мин силовых + 20 мин кардио (легкое)"
    else:
        return "🔥 Интенсивная тренировка: 30 мин кардио + 30 мин силовых"
