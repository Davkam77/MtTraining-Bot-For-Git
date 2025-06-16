from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.database import update_steps, get_steps_by_user

router = Router()

# Класс состояния
class StepsStates(StatesGroup):
    awaiting_steps = State()

@router.message(Command("steps"))
async def steps_handler(message: types.Message, state: FSMContext):
    await message.answer("🚶‍♂️ Введи количество шагов за сегодня:")
    await state.set_state(StepsStates.awaiting_steps)

@router.message(StateFilter(StepsStates.awaiting_steps), lambda msg: msg.text.isdigit())
async def handle_steps(message: types.Message, state: FSMContext):
    steps = int(message.text)
    user_id = message.from_user.id

    update_steps(user_id, steps)
    total = get_steps_by_user(user_id)

    await message.answer(f"✅ Принято! Сегодня ты прошёл {steps} шагов.\nОбщий счёт: {total} шагов 💪")
    await state.clear()

@router.message(StateFilter(StepsStates.awaiting_steps))
async def invalid_steps(message: types.Message, state: FSMContext):
    await message.answer("❌ Пожалуйста, введи только число — например: 7823")
