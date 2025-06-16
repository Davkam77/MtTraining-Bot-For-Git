from aiogram import Router, types
from aiogram.filters import Command
from utils.database import get_user_dashboard
from utils.workout_planner import generate_workout

router = Router()

@router.message(Command("workout"))
async def workout(message: types.Message):
    user_id = message.from_user.id
    stats = get_user_dashboard(user_id)

    if not stats["last_weight"]:
        await message.answer("⚠️ Добавь вес через /progress, чтобы получить тренировку.")
        return

    # Пока нет активности в базе — ставим среднюю
    activity = 1.38  
    workout_plan = generate_workout(activity)

    await message.answer(f"🏋️ <b>Твоя тренировка на сегодня:</b>\n\n{workout_plan}", parse_mode="HTML")
