from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("enable_steps"))
async def enable_steps(message: types.Message):
    text = (
        "📱 Для отслеживания шагов скачай приложение:\n"
        "• Google Fit — для Android и iOS: https://play.google.com/store/apps/details?id=com.google.android.apps.fitness\n"
        "• Apple Health — встроено на iPhone.\n\n"
        "🚶‍♂️ Каждый день смотри шаги в приложении и отправляй мне их с помощью /steps [кол-во_шагов].\n"
        "Например: /steps 8500\n"
        "Я рассчитаю, сколько ты потратил калорий!")
    await message.answer(text)


@router.message(Command("steps"))
async def steps(message: types.Message):
    try:
        steps = int(message.text.split(maxsplit=1)[1])
        calories = round(steps * 0.045, 1)  # Примерная формула
        text = (
            f"🎯 Ты прошёл {steps} шагов!\n"
            f"🔥 Примерно сжёг {calories} ккал.\n\n"
            "Молодец! Не забывай про ежедневную активность для лучшего результата.\n"
            "Если хочешь получать данные автоматически — установи Google Fit или Apple Health, смотри шаги там и сообщай мне!"
        )
    except (IndexError, ValueError):
        text = "❗ Введи количество шагов после команды: /steps 8500"
    await message.answer(text)
