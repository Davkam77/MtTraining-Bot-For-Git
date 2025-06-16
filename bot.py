import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import (
    advice, dashboard, help, mealplan, motivation,
    profile, progress, reset, start, steps, wake,
    weight, wizard, workout
)
from utils.database import init_db
from utils.scheduler import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ Переменная BOT_TOKEN не найдена в .env")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def register_all_handlers():
    dp.include_routers(
        start.router,
        help.router,
        wizard.router,
        mealplan.router,
        workout.router,
        progress.router,
        advice.router,
        wake.router,
        motivation.router,
        steps.router,
        weight.router,
        profile.router,
        reset.router,
        dashboard.router
    )

async def main():
    init_db()
    register_all_handlers()
    start_scheduler()
    print("✅ Бот запущен и слушает обновления...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
