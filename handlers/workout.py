from aiogram import Router, types
from aiogram.filters import Command
from utils.workout_loader import load_workout
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("workout"))
async def send_workout(message: types.Message):
    await message.answer("⏳ Получаю тренировку из архива...")
    workout = load_workout(message.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Другая тренировка", callback_data="new_workout")]
    ])
    await message.answer(workout, reply_markup=markup, parse_mode="HTML")

@router.callback_query(lambda c: c.data == "new_workout")
async def refresh_workout(callback: types.CallbackQuery):
    workout = load_workout(callback.from_user.id)
    await callback.message.edit_text(workout, reply_markup=callback.message.reply_markup, parse_mode="HTML")
    await callback.answer()
