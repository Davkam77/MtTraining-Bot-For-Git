from aiogram import Router, types
from aiogram.filters import Command
from utils.meal_api import get_meal_plan

router = Router()

@router.message(Command("mealplan"))
async def today_mealplan(message: types.Message):
    try:
        meal = get_meal_plan()

        await message.answer(
            f"<b>🍽️ Меню на сегодня:</b>\n\n{meal}\n\n💡 Это базовое меню. Можно адаптировать под себя.",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[ERROR] /mealplan: {e}")
        await message.answer("❗ Не удалось получить рацион. Попробуй позже.")
