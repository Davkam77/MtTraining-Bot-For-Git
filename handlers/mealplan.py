from aiogram import Router, types
from aiogram.filters import Command
from utils.database import get_user_profile, get_today_mealplan, save_mealplan
from utils.calorie_calc import calc_calories
from datetime import datetime

router = Router()

@router.message(Command("mealplan"))
async def mealplan_handler(message: types.Message):
    user_id = message.from_user.id
    profile = get_user_profile(user_id)

    if not profile:
        await message.answer("❗ Сначала заполни профиль через /wizard.")
        return

    # Проверим, есть ли сохранённое меню
    today_plan = get_today_mealplan(user_id)
    if today_plan:
        await message.answer(f"🍽️ Твоё меню на сегодня уже готово:\n\n{today_plan}")
        return

    kcal = calc_calories(**profile)
    breakfast = round(kcal * 0.3)
    lunch = round(kcal * 0.4)
    dinner = round(kcal * 0.3)

    text = (
        f"<b>🍽️ Меню на сегодня:</b>\n"
        f"🍳 Завтрак: {breakfast} ккал\n"
        f"🥗 Обед: {lunch} ккал\n"
        f"🍲 Ужин: {dinner} ккал\n\n"
        f"💡 Это базовое меню на день. Можно адаптировать под себя."
    )

    save_mealplan(user_id, datetime.now().strftime("%Y-%m-%d"), text)
    await message.answer(text, parse_mode="HTML")
