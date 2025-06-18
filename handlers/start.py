# handlers/start.py

from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 Привет! Я — твой персональный фитнес-бот.\n\n"
        "🎯 Что я умею:\n"
        "• 🏃 Отслеживать шаги и активность (подключи Google Fit)\n"
        "• 🍱 Предлагать рацион питания на день — /mealplan\n"
        "• 💪 Давать тренировку на каждый день — /workout\n"
        "• 💬 Присылать мотивацию — /motivation\n"
        "• 🤖 Давать советы по похудению — /advice\n"
        "• 📈 Следить за прогрессом — /progress\n\n"
        "⚙️ Сначала настрой план тренировок: /setworkout\n"
        "📊 Введи вес и рост: /weight\n"
        "❓ Полный список команд: /help\n\n"
        "📥 Для трекинга шагов — установи Google Fit:\n"
        "<a href='https://play.google.com/store/apps/details?id=com.google.android.apps.fitness'>Android</a>\n"
        "<a href='https://apps.apple.com/us/app/google-fit/id1433864494'>iOS</a>\n\n"
        "🚀 Готов? Начинай с /weight!"
    )
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)
