from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.database import add_user_metrics

router = Router()

class WeightStates(StatesGroup):
    await_age = State()
    await_height = State()
    await_weight = State()

@router.message(Command("weight"))
async def ask_age(message: types.Message, state: FSMContext):
    await state.set_state(WeightStates.await_age)
    await message.answer("🎂 Введи свой возраст (в годах):")

@router.message(WeightStates.await_age)
async def ask_height(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state(WeightStates.await_height)
        await message.answer("📏 Введи свой рост (в сантиметрах):")
    except ValueError:
        await message.answer("❗ Введи возраст числом, например: 25")

@router.message(WeightStates.await_height)
async def ask_weight(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        await state.update_data(height=height)
        await state.set_state(WeightStates.await_weight)
        await message.answer("⚖️ Введи свой вес (в кг):")
    except ValueError:
        await message.answer("❗ Введи рост числом, например: 175")

@router.message(WeightStates.await_weight)
async def save_all_metrics(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        data = await state.get_data()
        user_id = message.from_user.id
        age = data["age"]
        height = data["height"]
        add_user_metrics(user_id, age, height, weight)

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)

        if bmi < 18.5:
            category = "🔹 Недовес"
        elif bmi < 25:
            category = "✅ Норма"
        elif bmi < 30:
            category = "⚠️ Избыточный вес"
        else:
            category = "❗ Ожирение"

        await message.answer(
            f"✅ Данные сохранены!\n"
            f"Возраст: {age} лет\n"
            f"Рост: {height} см\n"
            f"Вес: {weight} кг\n\n"
            f"📊 <b>ИМТ: {bmi}</b>\n"
            f"{category}",
            parse_mode="HTML"
        )
        await state.clear()
    except ValueError:
        await message.answer("❗ Введи вес числом, например: 72.5")
