from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    text = (
        "🧠 <b>Помощь по боту MyTraining</b>\n\n"
        "<b>Доступные команды:</b>\n"
        "• <b>/start</b> — Запустить бота и пройти пошаговую настройку\n"
        "• <b>/wizard</b> — Перенастроить профиль (цель, параметры)\n"
        "• <b>/progress</b> — Посмотреть график изменения веса и прогноз\n"
        "• <b>/mealplan</b> — Получить персональное меню (бот сам считает калории)\n"
        "• <b>/workout</b> — Получить тренировку на сегодня\n"
        "• <b>/steps</b> — Узнать количество шагов за сегодня и сожжённые калории\n"
        "• <b>/enable_steps</b> — Подключить Google Fit для трекинга шагов\n"
        "• <b>/motivation</b> — Получить мотивацию на день (AI)\n"
        "• <b>/advice</b> — Спросить совет у AI-диетолога или тренера!\n\n"
        "🔗 <b>Шагомер (Google Fit)</b>:\n"
        "Чтобы бот мог отслеживать твои шаги автоматически — установи Google Fit на Android или iOS и дай доступ к шагам. /enable_steps всё подключит!\n\n"
        "💡 <b>Мотивация</b>:\n"
        "Каждый день получай мотивационный текст через /motivation — генерируется AI.\n\n"
        "Если не хочешь подключать шаги — просто игнорируй и пользуйся остальными функциями!\n"
        "Вопросы — всегда /help!")
    await message.answer(text, parse_mode="HTML")
