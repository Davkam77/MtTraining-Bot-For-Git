from aiogram import Router, types
from aiogram.filters import Command
from utils.database import get_today_mealplan
from utils.meal_generator import generate_mealplan_for_month

router = Router()

@router.message(Command("mealplan"))
async def today_mealplan(message: types.Message):
    user_id = message.from_user.id
    meals = get_today_mealplan(user_id)

    if not meals:
        generate_mealplan_for_month(user_id)
        meals = get_today_mealplan(user_id)

    await message.answer(
        f"<b>🍽️ Меню на сегодня:</b>\n\n"
        f"{meals}\n\n"
        f"💡 Это базовое меню на день. Можно адаптировать под себя.",
        parse_mode="HTML"
    )
