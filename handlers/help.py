from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    text = (
        "👋 Привет! Я — твой AI-тренер и помощник по питанию и движению.\n\n"
        "Вот что я умею:\n\n"
        "🍽️ *Хочешь есть, но не знаешь что?*\n"
        "• /mealplan — Составлю меню с калориями и БЖУ\n"
        "• /advice — Дай спрошу у AI-диетолога, что лучше\n\n"
        "🏋️ *Тренироваться без плана — путь в никуда!*\n"
        "• /workout — Придумаю тренировку на сегодня\n\n"
        "🚶 *Считаешь шаги?* Я тоже могу:\n"
        "• /steps — Введи сколько прошёл\n"
        "• /enable_steps — Подключу Google Fit, сам всё узнаю 😉\n\n"
        "📈 *Следишь за прогрессом?*\n"
        "• /progress — Покажу график веса и прогноз\n\n"
        "🔥 *Нужна мотивация?*\n"
        "• /motivation — AI знает, как взбодрить\n\n"
        "💡 Не бойся спрашивать. Напиши просто: _«хочу похудеть»_, _«какой перекус взять»_ — я пойму!\n\n"
        "❓ В любое время — просто /start чтобы начать заново или /wizard чтобы перенастроить цели.\n"
    )

    await message.answer(text, parse_mode="Markdown")
