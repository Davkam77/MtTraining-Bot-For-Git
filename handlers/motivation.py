# handlers/motivation.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.openai_advisor import ask_openai

router = Router()
scheduler = AsyncIOScheduler()


class MotivationStates(StatesGroup):
    awaiting_time = State()


# Сохраним расписание по chat_id
motivation_times = {}


@router.message(Command("motivation_time"))
async def cmd_set_motivation_time(message: types.Message, state: FSMContext):
    await message.answer(
        "⏰ В какое время ты хочешь получать мотивацию? Напиши в формате HH:MM (например, 09:00)."
    )
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
    motivation_times[chat_id] = (hour, minute)

    # Удаляем старую задачу, если была
    job_id = f"motivation_{chat_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    # Планируем мотивацию каждый день по выбранному времени
    scheduler.add_job(send_daily_motivation,
                      "cron",
                      hour=hour,
                      minute=minute,
                      args=[chat_id],
                      id=job_id,
                      replace_existing=True)
    await message.answer(f"🧠 Мотивация будет приходить каждый день в {text}!")
    await state.clear()


async def send_daily_motivation(chat_id):
    prompt = (
        "Сгенерируй короткое мотивационное сообщение для похудения, дисциплины, силы воли. "
        "Текст на русском, максимум 2 предложения, только по делу.")
    try:
        text = ask_openai(prompt)
    except Exception:
        text = "Сегодня — отличный день, чтобы стать лучше! 💪"
    # Здесь используем Bot.get_current() чтобы отправить вне хендлера
    from aiogram import Bot
    bot = Bot.get_current()
    await bot.send_message(chat_id, f"🔥 Мотивация дня:\n\n{text}")
