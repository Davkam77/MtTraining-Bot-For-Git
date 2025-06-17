# utils/workout_api.py
import os
import httpx
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import asyncio

load_dotenv()

API_KEY = os.getenv("GYM_API_KEY")
API_HOST = os.getenv("GYM_API_HOST")

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

BASE_URL = f"https://{API_HOST}/exercise"

async def translate_async(text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: GoogleTranslator(source='en', target='ru').translate(text))

async def get_random_exercises(count=5):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BASE_URL, headers=HEADERS)
            response.raise_for_status()
            all_exercises = response.json()

        if not isinstance(all_exercises, list):
            return "⚠️ Ответ не в ожидаемом формате."

        import random
        selected = random.sample(all_exercises, k=min(count, len(all_exercises)))
        result = []

        for ex in selected:
            name = await translate_async(ex.get("name", "Без названия"))
            equipment = await translate_async(ex.get("equipment", "собственное тело"))
            body_part = await translate_async(ex.get("bodyPart", "всё тело"))
            result.append(f"🔸 <b>{name}</b> ({body_part}, {equipment})")

        return "\n".join(result)

    except Exception as e:
        return f"❗ Ошибка при получении упражнений: {e}"
