import random
from datetime import datetime, timedelta
from utils.database import save_mealplan

BREAKFASTS = [
    "Овсянка с бананом и орехами",
    "Омлет с зеленью и хлебом",
    "Йогурт с мюсли и ягодами",
    "Тосты с авокадо и яйцом",
    "Творог с мёдом и орехами"
]

LUNCHES = [
    "Гречка с куриной грудкой и салатом",
    "Рис с овощами и индейкой",
    "Плов с телятиной и овощами",
    "Суп с чечевицей и хлебец",
    "Макароны с тунцом и зеленью"
]

DINNERS = [
    "Творог с ягодами и мёдом",
    "Овощное рагу с курицей",
    "Салат с яйцом и грецкими орехами",
    "Запечённая рыба с брокколи",
    "Овощной суп-пюре с хлебцами"
]

def generate_mealplan_for_month(user_id, days=30):
    today = datetime.now()
    for i in range(days):
        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        breakfast = random.choice(BREAKFASTS)
        lunch = random.choice(LUNCHES)
        dinner = random.choice(DINNERS)

        meals = (
            f"🍳 Завтрак: {breakfast}\n"
            f"🥗 Обед: {lunch}\n"
            f"🍲 Ужин: {dinner}"
        )

        save_mealplan(user_id, date, meals)
