import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")

def translate(text):
    return GoogleTranslator(source='en', target='ru').translate(text)

def fetch_meal(meal_type):
    url = "https://api.spoonacular.com/recipes/random"
    params = {
        "apiKey": API_KEY,
        "number": 1,
        "tags": meal_type,
        "includeNutrition": "true"
    }

    res = requests.get(url, params=params)
    res.raise_for_status()

    recipe = res.json()["recipes"][0]
    title_en = recipe["title"]
    title_ru = translate(title_en)
    calories = recipe["nutrition"]["nutrients"][0]["amount"]

    return f"{title_ru} — {round(calories)} ккал"

def get_meal_plan():
    breakfast = fetch_meal("breakfast")
    lunch = fetch_meal("lunch")
    dinner = fetch_meal("dinner")

    return (
        f"🍳 Завтрак: {breakfast}\n"
        f"🥗 Обед: {lunch}\n"
        f"🍲 Ужин: {dinner}"
    )
