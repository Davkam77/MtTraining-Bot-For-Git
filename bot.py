import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import (
 help, mealplan,  start, steps, wake,
    weight, workout, setworkout, motivation_router
)
from utils.database import init_db
from utils.scheduler import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена в .env")

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def register_all_handlers():
    dp.include_routers(
        start.router,
        help.router,
        mealplan.router,
        workout.router,
        wake.router,
        steps.router,
        weight.router,
        setworkout.router,
        motivation_router
    )


async def main():
    init_db()
    register_all_handlers()
    start_scheduler(bot)
    print("✅ Бот запущен и слушает обновления...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
