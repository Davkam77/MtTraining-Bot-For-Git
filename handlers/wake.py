# handlers/wake.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
from utils.scheduler import schedule_meal_reminders

router = Router()


class WakeStates(StatesGroup):
    awaiting_time = State()


@router.message(Command("wake"))
async def cmd_wake(message: types.Message, state: FSMContext):
    await message.answer(
        "⏰ Во сколько ты обычно просыпаешься? Напиши время в формате HH:MM (например, 07:30)."
    )
    await state.set_state(WakeStates.awaiting_time)


@router.message(WakeStates.awaiting_time)
async def process_wake_time(message: types.Message, state: FSMContext):
    text = message.text.strip()
    try:
        wake_time = datetime.strptime(text, "%H:%M").time()
    except ValueError:
        await message.answer("❌ Неверный формат! Введи время, например, 07:30")
        return

    # Ограничение по позднему питанию
    if wake_time.hour > 11:
        await message.answer(
            "⚠️ Поздний подъём! Не забудь, что приём пищи после 18–19:00 может мешать похудению. "
            "Лучше планировать ужин до 18:30!")

    # Сохраняем время для дальнейших напоминаний (можно в state или БД)
    await state.update_data(wake_time=text)

    # Планируем напоминания (см. функцию schedule_meal_reminders)
    await schedule_meal_reminders(message.chat.id, wake_time)

    await message.answer(
        f"⏰ Время пробуждения {text} сохранено! Бот будет присылать напоминания о завтраке и других приёмах пищи."
    )
    await state.clear()
