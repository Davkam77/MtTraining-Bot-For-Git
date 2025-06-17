from aiogram import Router, types
from aiogram.filters import Command
from utils.workout_api import get_ninjas_workout
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("workout"))
async def send_workout(message: types.Message):
    await message.answer("⏳ Получаю тренировку от API Ninjas...")
    workout = await get_ninjas_workout()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Хочу другую тренировку", callback_data="new_workout")]
    ])
    await message.answer(workout, reply_markup=markup, parse_mode="HTML")

@router.callback_query(lambda c: c.data == "new_workout")
async def refresh_workout(callback: types.CallbackQuery):
    workout = await get_ninjas_workout()
    await callback.message.edit_text(workout, reply_markup=callback.message.reply_markup, parse_mode="HTML")
    await callback.answer()
