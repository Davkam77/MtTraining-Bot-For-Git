from aiogram import Router, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from utils.database import (
    save_workout_settings,
    get_today_workout
)
from utils.workout_api import get_random_exercises

router = Router()

class WorkoutStates(StatesGroup):
    waiting_duration = State()
    waiting_months = State()

# 🔹 Команда /setworkout
@router.message(Command("setworkout"))
async def cmd_setworkout(message: Message, state: FSMContext):
    await message.answer("🏋️‍♂️ Сколько минут в день ты хочешь тренироваться?")
    await state.set_state(WorkoutStates.waiting_duration)

@router.message(WorkoutStates.waiting_duration)
async def process_duration(message: Message, state: FSMContext):
    try:
        duration = int(message.text)
        if duration <= 0 or duration > 180:
            raise ValueError
        await state.update_data(duration=duration)
        await message.answer("📅 Сколько месяцев будет длиться твой план?")
        await state.set_state(WorkoutStates.waiting_months)
    except ValueError:
        await message.answer("❗ Введи число от 1 до 180 (в минутах).")

@router.message(WorkoutStates.waiting_months)
async def process_months(message: Message, state: FSMContext):
    try:
        months = int(message.text)
        if months <= 0 or months > 12:
            raise ValueError
        data = await state.get_data()
        user_id = message.from_user.id
        save_workout_settings(user_id, data["duration"], months)
        await message.answer(
            f"✅ Готово!\n\n"
            f"Твой план на {months} месяцев по {data['duration']} минут в день сохранён!"
        )
        await state.clear()
    except ValueError:
        await message.answer("❗ Введи число от 1 до 12 (в месяцах).")

@router.message(Command("workout"))
async def cmd_workout(message: types.Message):
    user_id = message.from_user.id
    workout_text = get_random_exercises(count=5)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Хочу другую тренировку", callback_data="regen_workout")]
    ])

    await message.answer(
        f"<b>🏋️‍♂️ Твоя тренировка на сегодня:</b>\n\n{workout_text}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "regen_workout")
async def regenerate_workout(callback: types.CallbackQuery):
    workout_text = get_random_exercises(count=5)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Хочу другую тренировку", callback_data="regen_workout")]
    ])
    await callback.message.edit_text(
        f"<b>🏋️‍♂️ Новая тренировка:</b>\n\n{workout_text}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
