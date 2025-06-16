from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.openai_advisor import ask_openai
from utils.notifications import schedule_daily_motivation, add_user_for_motivation

router = Router()

class MotivationStates(StatesGroup):
    awaiting_time = State()

@router.message(Command("motivation"))
async def send_motivation(message: types.Message):
    prompt = (
        "Сгенерируй короткое мотивационное сообщение для похудения, дисциплины, силы воли. "
        "Текст на русском, максимум 2 предложения, только по делу."
    )
    try:
        text = await ask_openai(prompt)
    except Exception:
        text = "Сегодня — отличный день, чтобы стать лучше! 💪"
    await message.answer(f"🔥 Мотивация дня:\n\n{text}")

@router.message(Command("motivation_time"))
async def cmd_set_motivation_time(message: types.Message, state: FSMContext):
    await message.answer("⏰ В какое время ты хочешь получать мотивацию? Напиши в формате HH:MM (например, 09:00).")
    await state.set_state(MotivationStates.awaiting_time)

@router.message(MotivationStates.awaiting_time)
async def process_motivation_time(message: types.Message, state: FSMContext):
    text = message.text.strip()
    try:
        hour, minute = map(int, text.split(":"))
        assert 0 <= hour < 24 and 0 <= minute < 60
    except Exception:
        await message.answer("❌ Неверный формат! Введи время, например, 09:00")
        return

    chat_id = message.chat.id
    add_user_for_motivation(chat_id, hour, minute)
    await message.answer(f"🧠 Мотивация будет приходить каждый день в {text}!")
    await state.clear()
