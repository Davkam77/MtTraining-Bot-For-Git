# handlers/steps.py

from aiogram import Router, types
from aiogram.filters import Command
import random

router = Router()


@router.message(Command("steps"))
async def cmd_steps(message: types.Message):
    # В реальной интеграции здесь нужно получать данные пользователя из Google Fit API
    # Ниже — пример имитации для теста
    steps = random.randint(2000, 12000)
    calories = round(steps * 0.045, 1)  # Примерная формула: 0.045 ккал за шаг

    await message.answer(
        f"🚶‍♂️ Ты сегодня прошёл {steps} шагов и сжёг примерно {calories} ккал!\n\n"
        "👉 Чтобы получать реальные данные, подключи Google Fit на Android или iOS."
    )


@router.message(Command("enable_steps"))
async def enable_steps(message: types.Message):
    await message.answer(
        "📲 Для отслеживания шагов скачай Google Fit:\n"
        "https://play.google.com/store/apps/details?id=com.google.android.apps.fitness\n\n"
        "Дай доступ к данным о шагах. Скоро бот сможет показывать реальную статистику.\n"
        "Если не хочешь — просто пропусти этот шаг.")
