from aiogram import Router, types
from aiogram.filters import Command
from utils.workout_loader import load_workout
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from utils.workout_loader import generate_workout as get_today_workout_text
from aiogram.types import CallbackQuery

router = Router()

@router.message(Command("workout"))
async def send_workout(message: types.Message):
    await message.answer("⏳ Получаю тренировку из архива...")
    workout = load_workout(message.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Другая тренировка", callback_data="new_workout")]
    ])
    await message.answer(workout, reply_markup=markup, parse_mode="HTML")

@router.callback_query(lambda c: c.data == "refresh_workout")
async def refresh_workout(callback: CallbackQuery):
    workout = get_today_workout_text()  # или как у тебя функция называется
    try:
        await callback.message.edit_text(
            workout,
            reply_markup=callback.message.reply_markup,
            parse_mode="HTML"
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass  # просто игнорируем
        else:
            raise e  # если другая ошибка — пробрасываем