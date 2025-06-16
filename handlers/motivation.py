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
    prompt = "Сгенерируй короткое мотивационное сообщение для похудения, дисциплины, силы воли. На русском, до 2 предложений."
    try:
        text = await ask_openai(prompt)
    except:
        text = "Сегодня — отличный день, чтобы стать лучше! 💪"
    await message.answer(f"🔥 Мотивация дня:\n\n{text}")

@router.message(Command("motivation_time"))
async def cmd_set_motivation_time(message: types.Message, state: FSMContext):
    await message.answer("⏰ Во сколько присылать мотивацию? Введи время в формате HH:MM (например, 08:00)")
    await state.set_state(MotivationStates.awaiting_time)

@router.message(MotivationStates.awaiting_time)
async def process_motivation_time(message: types.Message, state: FSMContext):
    try:
        hour, minute = map(int, message.text.strip().split(":"))
        assert 0 <= hour < 24 and 0 <= minute < 60
    except:
        await message.answer("❗ Введи корректное время, например: 07:30")
        return

    add_user_for_motivation(message.chat.id, hour, minute)
    await message.answer(f"✅ Готово! Теперь мотивация будет приходить в {hour:02}:{minute:02}")
    await state.clear()

def get_daily_motivation():
    return "Сегодня отличный день, чтобы стать сильнее! 💪"
