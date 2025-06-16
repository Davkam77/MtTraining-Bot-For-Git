from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()
user_meal_jobs = {}

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

async def schedule_meal_reminders(chat_id, wake_time):
    from utils.scheduler import remove_meal_jobs, send_notification

    remove_meal_jobs(chat_id)
    base = datetime.combine(datetime.today(), wake_time)

    plan = [
        ("🥣 Завтрак", base + timedelta(hours=2)),
        ("🍏 Перекус", base + timedelta(hours=5)),
        ("🍲 Обед", base + timedelta(hours=7)),
        ("💪 Тренировка", base + timedelta(hours=9)),
        ("🍽️ Ужин", base + timedelta(hours=11)),
    ]

    jobs = []
    for title, time in plan:
        if time.time() <= datetime.strptime("18:30", "%H:%M").time():
            job = scheduler.add_job(send_notification, "date", run_date=time, args=[chat_id, title])
            jobs.append(job)

    user_meal_jobs[chat_id] = jobs

def remove_meal_jobs(chat_id):
    for job in user_meal_jobs.get(chat_id, []):
        try:
            job.remove()
        except:
            pass
    user_meal_jobs[chat_id] = []

async def send_notification(chat_id, text):
    bot = Bot.get_current()
    await bot.send_message(chat_id, text)
