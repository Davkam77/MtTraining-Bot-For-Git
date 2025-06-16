from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.calorie_calc import calc_calories
from utils.database import get_user_profile

router = Router()

@router.message(Command("profile"))
async def profile_handler(message: types.Message):
    user_id = message.from_user.id
    data = get_user_profile(user_id)

    if not data:
        await message.answer("❗ Профиль не найден. Запусти /wizard.")
        return

    kcal = calc_calories(
        weight=data["weight"],
        height=data["height"],
        age=data["age"],
        gender=data["gender"],
        activity=data["activity"],
        goal=data["goal"]
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="♻️ Перенастроить", callback_data="profile_reset")],
        [InlineKeyboardButton(text="📈 Прогресс", callback_data="profile_progress")],
        [InlineKeyboardButton(text="🍽️ Меню", callback_data="profile_mealplan")],
    ])

    await message.answer(
        f"🧍‍♂️ <b>Твой профиль</b>:\n\n"
        f"🔹 Вес: <b>{data['weight']} кг</b>\n"
        f"🔹 Цель: <b>{data['goal']} кг</b>\n"
        f"🔹 Рост: <b>{data['height']} см</b>\n"
        f"🔹 Возраст: <b>{data['age']}</b>\n"
        f"🔹 Пол: <b>{'Мужской' if data['gender'] == 'm' else 'Женский'}</b>\n"
        f"🔹 Активность: <b>{data['activity']}</b>\n"
        f"🔹 Реком. калории: <b>{round(kcal)} ккал/день</b>",
        parse_mode="HTML",
        reply_markup=kb
    )

@router.callback_query(F.data == "profile_reset")
async def cb_reset(call: types.CallbackQuery):
    await call.message.answer("🔁 Чтобы перенастроить профиль — запусти /wizard")
    await call.answer()

@router.callback_query(F.data == "profile_progress")
async def cb_progress(call: types.CallbackQuery):
    await call.message.answer("📊 Введи /progress для графика веса.")
    await call.answer()

@router.callback_query(F.data == "profile_mealplan")
async def cb_mealplan(call: types.CallbackQuery):
    await call.message.answer("🍽️ Введи /mealplan для просмотра меню.")
    await call.answer()
