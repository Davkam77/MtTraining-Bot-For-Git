from aiogram import Bot
import os
from dotenv import load_dotenv
from utils.user_settings import get_user_plan
from utils.workout_loader import load_workout
from utils.motivation_loader import get_random_motivation
from utils.meal_api import get_meal_plan

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TELEGRAM_BOT_TOKEN")


bot = Bot(token=TELEGRAM_TELEGRAM_BOT_TOKEN)

async def send_daily_push(user_id: int):
    motivation = get_random_motivation()
    workout = load_workout(user_id)
    meal = await get_meal_plan()

    message = f"<b>🔥 Утренний заряд!</b>\n\n" \
              f"<b>💬 Мотивация:</b> {motivation}\n\n" \
              f"<b>🍽 Рацион:</b>\n{meal}\n\n" \
              f"<b>🏋️ Тренировка:</b>\n{workout}"

    await bot.send_message(user_id, message, parse_mode="HTML")
