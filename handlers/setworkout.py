from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.user_settings import set_user_plan

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
    duration_str = callback.data  # например: "45 мин"
    duration = int(duration_str.split()[0])  # -> 45

    plan_key = {
        "1 month": "1_month",
        "3 months": "3_months",
        "6 months": "6_months"
    }.get(plan, "1_month")

    set_user_plan(callback.from_user.id, plan_key, duration)
    await callback.message.edit_text(f"✅ План сохранён: {plan_key}, {duration} мин в день!")
    await state.clear()
