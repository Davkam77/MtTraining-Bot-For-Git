import json
import random
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

with open("data/motivations.json", "r", encoding="utf-8") as f:
    MOTIVATIONS = json.load(f)

@router.message(Command("motivation"))
async def send_motivation(message: Message):
    motivation_text = random.choice(MOTIVATIONS)
    await message.answer(motivation_text)
