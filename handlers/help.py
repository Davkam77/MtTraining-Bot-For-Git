from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: Message):
    text = (
        "🤖 <b>Возможности бота:</b>\n\n"
        "🔹 <b>/start</b> — начать или перезапустить\n"
        "🔹 <b>/setworkout</b> — задать план тренировок\n"
        "🔹 <b>/setweight</b> — ввести вес\n"
        "🔹 <b>/progress</b> — посмотреть прогресс\n"
        "🔹 <b>/motivation</b> — мотивация дня\n"
        "🔹 <b>/mealplan</b> — рацион на сегодня\n"
        "🔹 <b>/workout</b> — тренировка дня\n"
        "🔹 <b>/status</b> — статистика шагов и веса\n\n"
        "ℹ️ Тренировки подстраиваются под твои цели и время.\n"
        "💡 Открывай бота утром — и получай мотивацию, еду и тренировку!"
    )

    await message.answer(text, parse_mode="HTML")
