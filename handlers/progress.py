from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from utils.chart_generator import generate_chart_human

router = Router()


@router.message(Command("progress"))
async def cmd_progress(message: types.Message):
    result = generate_chart_human(message.from_user.id)
    if result:
        photo, trend_text = result
        photo.seek(0)
        input_file = BufferedInputFile(photo.read(), filename="progress.png")
        caption = f"📉 Прогресс веса\n{trend_text}"
        await message.answer_photo(input_file, caption=caption)
    else:
        await message.answer(
            "❗ У тебя пока нет сохранённых данных веса. Введи: /weight 99.5")
