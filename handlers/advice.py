from aiogram import Router, types
from aiogram.filters import Command
from utils.openai_advisor import ask_openai

router = Router()

@router.message(Command("advice"))
async def advice_answer(message: types.Message):
    await message.answer("💬 Думаю над советом...")

    question = "Дай полезный совет по здоровому питанию и образу жизни"
    answer = await ask_openai(question)

    await message.answer(f"🧠 Совет от AI:\n\n{answer}")
