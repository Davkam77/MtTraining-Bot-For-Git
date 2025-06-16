from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from datetime import datetime, timedelta
from handlers.motivation import get_daily_motivation
from utils.workout_generator import generate_daily_workout
from utils.database import get_all_users
from utils.database import get_today_mealplan 

scheduler = AsyncIOScheduler()
user_meal_jobs = {}

def start_scheduler(bot: Bot):
    if not scheduler.running:
        scheduler.add_job(morning_push, 'cron', hour=8, minute=0, args=[bot])
        scheduler.start()

async def morning_push(bot: Bot):
    users = get_all_users()
    for user_id in users:
        try:
            motivation = ()
            meals = get_today_mealplan(user_id)
            workout = generate_daily_workout(user_id)

            msg = (
                f"🌞 Доброе утро!\n\n"
                f"💬 *Мотивация дня:*\n_{motivation}_\n\n"
                f"🍽️ *Рацион дня:*\n{meals}\n\n"
                f"🏋️ *Тренировка дня:*\n{workout}"
            )

            await bot.send_message(user_id, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"[!] Ошибка для {user_id}: {e}")

async def schedule_meal_reminders(chat_id, wake_time):
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
