# utils/workout_api.py
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NINJAS_API_KEY")
HEADERS = {
    "X-Api-Key": API_KEY
}
BASE_URL = "https://api.api-ninjas.com/v1/exercises"

async def get_ninjas_workout():
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "muscle": "biceps",
                "type": "strength",
                "difficulty": "beginner"
            }
            async with session.get(BASE_URL, headers=HEADERS, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        return format_workout(data)
                    # fallback без параметров
                async with session.get(BASE_URL, headers=HEADERS) as fallback:
                    fallback_data = await fallback.json()
                    return format_workout(fallback_data[:5])
    except Exception as e:
        return f"❗ Ошибка при получении упражнений: {e}"

def format_workout(data):
    lines = []
    for ex in data[:5]:
        name = ex.get("name", "Без названия")
        muscle = ex.get("muscle", "мышцы")
        eq = ex.get("equipment", "собственное тело")
        lines.append(f"🔹 <b>{name}</b> ({muscle}, {eq})")
    return "\n".join(lines)
