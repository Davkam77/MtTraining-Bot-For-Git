from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InputFile
from utils.chart_generator import generate_chart
from aiogram.types import BufferedInputFile

router = Router()

@router.message(Command("progress"))
async def cmd_progress(message: types.Message):
    photo = generate_chart(message.from_user.id)
    if photo:
        photo.seek(0)  # обязательно сбросить указатель в начало!
        input_file = BufferedInputFile(photo.read(), filename="progress.png")
        await message.answer_photo(input_file, caption="📉 Твой график веса")
    else:
        await message.answer("❗ У тебя пока нет сохранённых данных веса. Введи: /weight 99.5")
