from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.database import add_weight_entry

router = Router()

class WeightStates(StatesGroup):
    await_weight = State()

@router.message(Command("weight"))
async def ask_weight(message: types.Message, state: FSMContext):
    await state.set_state(WeightStates.await_weight)
    await message.answer("⚖️ Введи текущий вес (в кг):")

@router.message(WeightStates.await_weight)
async def save_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        user_id = message.from_user.id
        add_weight_entry(user_id, weight)
        await message.answer(f"✅ Вес {weight} кг сохранён!")
        await state.clear()
    except ValueError:
        await message.answer("❗ Введи вес числом, например: 84.2")
