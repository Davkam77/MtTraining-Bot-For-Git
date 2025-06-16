# utils/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram import Bot

scheduler = AsyncIOScheduler()  # создаём, но НЕ стартуем!


def start_scheduler():
    if not scheduler.running:
        scheduler.start()  # запускать только когда loop уже есть!


# Можно хранить расписания в памяти, но для продакшна — использовать БД.
user_meal_jobs = {}


async def schedule_meal_reminders(chat_id, wake_time):
    """
    Планирует уведомления о приёмах пищи для пользователя с учётом wake_time.
    Уведомляет: завтрак, перекус, обед, тренировка, ужин (но не позже 18:30).
    """
    remove_meal_jobs(chat_id)
    jobs = []

    base = datetime.combine(datetime.today(), wake_time)
    meal_plan = [
        ("🥣 Время завтракать!", base + timedelta(hours=2)),
        ("🍏 Лёгкий перекус.", base + timedelta(hours=5)),
        ("🍲 Обед!", base + timedelta(hours=7)),
        ("💪 Время размяться или тренировка.", base + timedelta(hours=9)),
        ("🍽️ Лёгкий ужин (не позже 18:30)!", base + timedelta(hours=11)),
    ]

    # Ограничение ужина не позже 18:30
    for title, dt in meal_plan:
        if dt.time() > datetime.strptime("18:30", "%H:%M").time():
            continue
        job = scheduler.add_job(send_notification,
                                "date",
                                run_date=dt,
                                args=[chat_id, title])
        jobs.append(job)

    user_meal_jobs[chat_id] = jobs


def remove_meal_jobs(chat_id):
    jobs = user_meal_jobs.get(chat_id, [])
    for job in jobs:
        try:
            job.remove()
        except Exception:
            pass
    user_meal_jobs[chat_id] = []


async def send_notification(chat_id, text):
    bot = Bot.get_current()
    await bot.send_message(chat_id, text)
