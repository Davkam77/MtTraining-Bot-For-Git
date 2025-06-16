from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.calorie_calc import calc_calories
from utils.database import save_user_profile, add_weight_entry

router = Router()

class WizardStates(StatesGroup):
    await_weight = State()
    await_goal = State()
    await_height = State()
    await_age = State()
    await_gender = State()
    await_activity = State()
    done = State()

@router.message(Command("wizard"))
async def wizard_start(message: types.Message, state: FSMContext):
    await message.answer("1️⃣ Введи текущий вес (в кг):")
    await state.set_state(WizardStates.await_weight)

@router.message(WizardStates.await_weight)
async def wizard_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        await state.update_data(weight=weight)
        add_weight_entry(message.from_user.id, weight)  # Сохраняем в БД
        await state.set_state(WizardStates.await_goal)
        await message.answer("2️⃣ Введи желаемый вес (кг):")
    except:
        await message.answer("❗ Введи вес числом, например: 86.4")

@router.message(WizardStates.await_goal)
async def wizard_goal(message: types.Message, state: FSMContext):
    try:
        goal = float(message.text.replace(",", "."))
        await state.update_data(goal=goal)
        await state.set_state(WizardStates.await_height)
        await message.answer("3️⃣ Введи рост (см):")
    except:
        await message.answer("❗ Введи желаемый вес числом, например: 75")

@router.message(WizardStates.await_height)
async def wizard_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        await state.update_data(height=height)
        await state.set_state(WizardStates.await_age)
        await message.answer("4️⃣ Сколько тебе лет?")
    except:
        await message.answer("❗ Введи рост в сантиметрах, например: 178")

@router.message(WizardStates.await_age)
async def wizard_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Мужчина", callback_data="gender_m")],
            [InlineKeyboardButton(text="Женщина", callback_data="gender_f")]
        ])
        await state.set_state(WizardStates.await_gender)
        await message.answer("5️⃣ Укажи пол:", reply_markup=kb)
    except:
        await message.answer("❗ Введи возраст числом, например: 27")

@router.callback_query(WizardStates.await_gender, F.data.in_(["gender_m", "gender_f"]))
async def wizard_gender(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(gender=call.data[-1])
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сидячий", callback_data="activity_1.2")],
        [InlineKeyboardButton(text="Умеренный", callback_data="activity_1.38")],
        [InlineKeyboardButton(text="Активный", callback_data="activity_1.55")]
    ])
    await state.set_state(WizardStates.await_activity)
    await call.message.answer("6️⃣ Какой у тебя уровень активности?", reply_markup=kb)

@router.callback_query(WizardStates.await_activity, F.data.startswith("activity_"))
async def wizard_activity(call: types.CallbackQuery, state: FSMContext):
    activity = float(call.data.split("_")[1])
    await state.update_data(activity=activity)
    data = await state.get_data()

    # Сохраняем профиль в БД
    save_user_profile(
        user_id=call.from_user.id,
        weight=data["weight"],
        goal=data["goal"],
        height=data["height"],
        age=data["age"],
        gender=data["gender"],
        activity=activity
    )

    kcal = calc_calories(
        weight=data["weight"],
        height=data["height"],
        age=data["age"],
        gender=data["gender"],
        activity=activity,
        goal=data["goal"]
    )

    await call.message.answer(
        f"✅ Всё готово!\n\n"
        f"🎯 Цель: <b>{data['goal']} кг</b>\n"
        f"🔥 Реком. калории: <b>{round(kcal)} ккал/день</b>\n\n"
        f"Команды: /progress /mealplan /dashboard"
    , parse_mode="HTML")

    await state.set_state(WizardStates.done)
