# bot.py

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import asyncio
import os
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
import logging
from utils.scheduler import start_scheduler

# Подключаем все обработчики
from handlers import start, help, wizard, mealplan, workout, progress, advice, wake, motivation, steps
from utils import scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env!")

bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def register_all_handlers():
    dp.include_routers(start.router, help.router, wizard.router,
                       mealplan.router, workout.router, progress.router,
                       advice.router, wake.router, motivation.router,
                       steps.router)


async def main():
    register_all_handlers()
    start_scheduler()  # Только тут! После запуска event loop!
    print("✅ Бот запущен и слушает обновления...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
