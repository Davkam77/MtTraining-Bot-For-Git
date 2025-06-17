from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

class SetWorkoutState(StatesGroup):
    plan = State()
    duration = State()

@router.message(F.text == "/setworkout")
async def start_set_workout(message: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    for label in ["1 month", "3 months", "6 months"]:
        kb.button(text=label, callback_data=label)
    await message.answer("📅 Выберите длительность плана:", reply_markup=kb.as_markup())
    await state.set_state(SetWorkoutState.plan)

@router.callback_query(SetWorkoutState.plan)
async def choose_plan(callback: CallbackQuery, state: FSMContext):
    await state.update_data(plan=callback.data)
    kb = InlineKeyboardBuilder()
    for label in ["15 мин", "30 мин", "45 мин", "60 мин"]:
        kb.button(text=label, callback_data=label)
    await callback.message.edit_text("⏱️ Сколько минут в день хотите тренироваться?", reply_markup=kb.as_markup())
    await state.set_state(SetWorkoutState.duration)

@router.callback_query(SetWorkoutState.duration)
async def confirm_plan(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    plan = data.get("plan")
    duration = callback.data
    await callback.message.edit_text(f"✅ План сохранён: {plan}, {duration} в день!")
    await state.clear()
