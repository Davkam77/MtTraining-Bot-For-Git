from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("workout"))
async def workout_handler(message: types.Message):
    await message.answer(
        "🏋️‍♂️ Пример тренировки:\n"
        "— Приседания 3x15\n"
        "— Отжимания 3x12\n"
        "— Планка 3x30 сек\n"
        "— Кардио: 30 мин ходьбы"
    )
