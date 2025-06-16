from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.database import update_steps, get_steps_by_user

router = Router()

@router.message(Command("steps"))
async def steps_handler(message: types.Message, state: FSMContext):
    await message.answer("🚶‍♂️ Введи количество шагов за сегодня:")
    await state.set_state("awaiting_steps")

@router.message(lambda msg: msg.text.isdigit(), state="awaiting_steps")
async def handle_steps(message: types.Message, state: FSMContext):
    steps = int(message.text)
    user_id = message.from_user.id

    update_steps(user_id, steps)
    total = get_steps_by_user(user_id)

    await message.answer(f"✅ Принято! Сегодня ты прошёл {steps} шагов.\nОбщий счёт: {total} шагов 💪")
    await state.clear()

@router.message(state="awaiting_steps")
async def invalid_steps(message: types.Message, state: FSMContext):
    await message.answer("❌ Пожалуйста, введи только число — например: 7823")
