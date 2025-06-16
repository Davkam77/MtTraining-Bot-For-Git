from aiogram import Router, types
from aiogram.filters import Command
from utils.database import get_user_dashboard

router = Router()

@router.message(Command("dashboard"))
async def show_dashboard(message: types.Message):
    user_id = message.from_user.id
    stats = get_user_dashboard(user_id)

    if stats["total_entries"] == 0:
        await message.answer("📭 Пока нет данных о весе. Добавь свой текущий вес через /weight.")
        return

    delta = None
    if stats["first_weight"] and stats["last_weight"]:
        delta = round(stats["last_weight"] - stats["first_weight"], 1)

    trend = "📉 Похудел" if delta and delta < 0 else "📈 Набрал" if delta else "—"

    await message.answer(
        f"<b>📊 Прогресс:</b>\n\n"
        f"🗓️ Последняя запись: <b>{stats['last_date']}</b>\n"
        f"⚖️ Вес: <b>{stats['last_weight']} кг</b>\n"
        f"📦 Изменение с начала: <b>{delta} кг</b>\n"
        f"{trend}\n\n"
        f"Всего записей: <b>{stats['total_entries']}</b>\n"
        f"Добавить вес — /weight"
    )
