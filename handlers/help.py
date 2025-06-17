from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def send_help(message: types.Message):
    text = (
        "<b>💪 Добро пожаловать в MtTraining Bot!</b>\n\n"
        "Вот что ты можешь делать:\n\n"
        "/start — Перезапуск бота\n"
        "/workout — Получить сегодняшнюю тренировку\n"
        "/mealplan — Предложение по рациону\n"
        "/motivation — Мотивационная цитата\n"
        "/wake — Настроить утреннюю рассылку\n"
        "/setworkout — Настроить длительность и время тренировок\n"
        "/help — Это меню помощи\n\n"
        "🧠 Тренировки и еда подстраиваются под твои цели!"
    )
    await message.answer(text, parse_mode="HTML")
