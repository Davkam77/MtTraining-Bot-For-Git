from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.scheduler import schedule_meal_reminders

router = Router()

@router.message(Command("wake"))
async def wake_handler(message: types.Message, state: FSMContext):
    await message.answer("Во сколько ты просыпаешься? Напиши в формате HH:MM (например, 07:30).")

    await state.set_state("awaiting_wake_time")

@router.message(lambda msg: msg.text and ":" in msg.text)
async def handle_wake_time(message: types.Message, state: FSMContext):
    wake_time = message.text.strip()

    try:
        schedule_meal_reminders(wake_time)
        await state.clear()
        await message.answer(f"Отлично! Будильник установлен на {wake_time}. Я напомню о питании вовремя 💪")
    except ValueError:
        await message.answer("Неверный формат времени. Попробуй снова, например: 07:30.")
