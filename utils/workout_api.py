# utils/workout_api.py
import requests
import random
from deep_translator import GoogleTranslator

API_KEY = "a29f6566d6mshbfaa09065ae45aep1e162djsn728bd1750765"
API_HOST = "exercise-db-fitness-workout-gym.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

BASE_URL = f"https://{API_HOST}/exercises"


def translate(text):
    return GoogleTranslator(source='en', target='ru').translate(text)


def get_random_exercises(count=5):
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        all_exercises = response.json()

        selected = random.sample(all_exercises, k=count)
        result = []

        for ex in selected:
            name = translate(ex["name"])
            equipment = translate(ex.get("equipment", "собственное тело"))
            body_part = translate(ex.get("bodyPart", "всё тело"))
            result.append(f"🔸 <b>{name}</b> ({body_part}, {equipment})")

        return "\n".join(result)

    except Exception as e:
        return f"❗ Ошибка при получении упражнений: {e}"
