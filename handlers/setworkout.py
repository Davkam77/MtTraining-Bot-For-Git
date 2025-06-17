from aiogram import Router, types, F
from aiogram.filters import Command
from utils.user_settings import set_user_plan

router = Router()
available = ["1_month", "3_months", "6_months"]

@router.message(Command("setworkout"))
async def ask_for_plan(message: types.Message):
    await message.answer("Введите длительность плана (варианты: 1_month, 3_months, 6_months):")

@router.message(F.text.in_(available))
async def save_plan(message: types.Message):
    set_user_plan(message.from_user.id, message.text.strip())
    await message.answer(f"✅ План <b>{message.text}</b> сохранён!", parse_mode="HTML")
