from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("mealplan"))
async def mealplan_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    kcal = int(data.get("kcal", 2000))
    await message.answer(
        f"🍽️ Пример меню на {kcal} ккал:\n"
        f"Завтрак: яйца, овсянка (20%)\n"
        f"Обед: курица, гречка (30%)\n"
        f"Ужин: рыба, овощи (25%)\n"
        f"Перекусы: творог, орехи, фрукты (25%)"
    )
