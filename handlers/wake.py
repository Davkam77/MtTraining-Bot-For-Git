from aiogram import Router, types, F
from aiogram.filters import Command
from utils.user_settings import load_settings, save_settings
from utils.scheduler import schedule_daily_push

router = Router()

@router.message(Command("wake"))
async def set_wake_time(message: types.Message):
    await message.answer("Во сколько напоминать каждый день? (формат HH:MM, например 08:30)")

@router.message(F.text.regexp(r"^\d{2}:\d{2}$"))
async def save_wake_time(message: types.Message):
    user_id = str(message.from_user.id)
    time = message.text.strip()

    settings = load_settings()
    settings[user_id] = settings.get(user_id, {})
    settings[user_id]["wake_time"] = time
    save_settings(settings)

    # ⏰ Запускаем задачу для пользователя
    schedule_daily_push(user_id, time)

    await message.answer(f"✅ Напоминания будут каждый день в <b>{time}</b>", parse_mode="HTML")
