# handlers/start.py

from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 Привет! Я помогу тебе похудеть быстро и без заморочек.\n\n"
        "✨ Доступные функции:\n"
        "— 🏃 Отслеживание шагов (/steps) + Google Fit\n"
        "— 🍽️ Меню и калории (/mealplan)\n"
        "— 💪 Тренировка дня (/workout)\n"
        "— 💡 Мотивация каждый день (/motivation)\n"
        "— 🤖 Совет от AI (/advice)\n\n"
        "⚙️ Настрой профиль: /wizard\n"
        "❓ Помощь по всем командам: /help\n\n"
        "Для трекинга шагов — скачай Google Fit:\n"
        "<a href='https://play.google.com/store/apps/details?id=com.google.android.apps.fitness'>Android</a>\n"
        "<a href='https://apps.apple.com/us/app/google-fit/id1433864494'>iOS</a>"
    )
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)
