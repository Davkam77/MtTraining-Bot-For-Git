from aiogram import Router, types
from aiogram.filters import Command
from utils.database import get_user_dashboard
from utils.meal_generator import generate_mealplan
from utils.calorie_calc import calc_calories

router = Router()

@router.message(Command("mealplan"))
async def mealplan(message: types.Message):
    user_id = message.from_user.id
    stats = get_user_dashboard(user_id)

    if not stats["last_weight"]:
        await message.answer("⚠️ Добавь хотя бы один вес через /progress, чтобы мы могли рассчитать рацион.")
        return

    # Примитивные значения (можно улучшить, если есть сохранённые параметры)
    weight = stats["last_weight"]
    height = 170
    age = 27
    gender = 'm'
    activity = 1.38
    goal = weight - 3  # худеем

    kcal = calc_calories(weight, height, age, gender, activity, goal)
    meals = generate_mealplan(kcal)

    text = f"🍽️ <b>Твой рацион на сегодня (~{int(kcal)} ккал):</b>\n\n"
    for meal, desc in meals.items():
        text += f"▪️ <b>{meal}</b>: {desc}\n"
    
    await message.answer(text, parse_mode="HTML")
