from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from handlers.wizard import WizardStates

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 Привет! Я помогу тебе похудеть быстро и без лишних заморочек.\n\n"
        "✨ Теперь доступно:\n"
        "— 🏃 Отслеживание шагов (/steps), интеграция с Google Fit (Android/iOS)\n"
        "— 💡 Мотивационные напоминания каждый день (/motivation)\n\n"
        "Чтобы шагомер работал автоматически, скачай Google Fit: "
        "<a href='https://play.google.com/store/apps/details?id=com.google.android.apps.fitness'>Google Fit на Android</a>\n"
        "<a href='https://apps.apple.com/us/app/google-fit/id1433864494'>Google Fit на iOS</a>\n"
        "Включи шагомер: /enable_steps\n\n"
        "Для персональных советов и рациона — используй /wizard, /mealplan, /progress, /advice\n"
        "В любой момент — /help")
    await message.answer(text,
                         parse_mode="HTML",
                         disable_web_page_preview=True)
