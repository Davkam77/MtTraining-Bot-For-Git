from aiogram import Router, types
from aiogram.filters import Command
from utils.motivation_loader import get_daily_motivation

router = Router()

@router.message(Command("motivation"))
async def motivation_handler(message: types.Message):
    text = get_daily_motivation()
    await message.answer(f"<b>💬 Мотивация дня:</b>\n\n<i>{text}</i>", parse_mode="HTML")
