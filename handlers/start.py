from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from handlers.wizard import WizardStates

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я помогу тебе похудеть быстро и без лишних заморочек.\n\n"
        "Давай настроим твой профиль.\n\n"
        "⏳ Ответь на пару вопросов или нажми /wizard для настройки в любой момент!"
    )
    await state.set_state(WizardStates.await_weight)
    await message.answer("1️⃣ Введи твой текущий вес (кг):")
