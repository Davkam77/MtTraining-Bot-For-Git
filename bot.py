# bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
import asyncio
import os
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
import logging
from handlers import start, help, wizard, mealplan, workout, progress, advice


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def register_all_handlers():
    dp.include_routers(
        start.router,
        help.router,
        wizard.router,
        mealplan.router,
        workout.router,
        progress.router,
        advice.router
    )

async def main():
    register_all_handlers()
    print("✅ Бот запущен и слушает обновления...")  # <--- добавь эту строку
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
