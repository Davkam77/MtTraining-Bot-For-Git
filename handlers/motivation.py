from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import json
import random
from database import get_db_connection

router = Router()

# Загружаем мотивации из файла в папке data/
filepath = "data/motivations.json"
with open(filepath, "r", encoding="utf-8") as f:
    MOTIVATIONS = json.load(f)

@router.message(Command("motivation"))
async def send_motivation(message: types.Message):
    user_id = message.from_user.id

    if not MOTIVATIONS:
        await message.answer("Нет мотивационных фраз.")
        return

    motivation_text = random.choice(MOTIVATIONS)
    await message.answer(motivation_text)

    # Сохраняем в базу данных
    db = get_db_connection()
    query = "INSERT INTO motivation_history (user_id, motivation_text, timestamp) VALUES (?, ?, ?)"
    db.execute(query, (user_id, motivation_text, datetime.utcnow()))
    db.commit()
    db.close()
