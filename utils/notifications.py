from aiogram import Bot
from utils.openai_advisor import ask_openai

motivation_users = {}  # chat_id: (hour, minute)


def add_user_for_motivation(chat_id, hour, minute):
    motivation_users[chat_id] = (hour, minute)
    schedule_daily_motivation(chat_id, hour, minute)


def schedule_daily_motivation(chat_id, hour, minute):
    from utils.scheduler import scheduler
    job_id = f"motivation_{chat_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(send_daily_motivation,
                      "cron",
                      hour=hour,
                      minute=minute,
                      args=[chat_id],
                      id=job_id,
                      replace_existing=True)


async def send_daily_motivation(chat_id):
    prompt = (
        "Сгенерируй короткое мотивационное сообщение для похудения, дисциплины, силы воли. "
        "Текст на русском, максимум 2 предложения, только по делу.")
    try:
        text = await ask_openai(prompt)
    except Exception:
        text = "Сегодня — отличный день, чтобы стать лучше! 💪"
    bot = Bot.get_current()
    await bot.send_message(chat_id, f"🔥 Мотивация дня:\n\n{text}")
