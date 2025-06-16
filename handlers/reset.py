from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.database import get_connection

router = Router()

@router.message(Command("reset"))
async def reset_handler(message: types.Message):
    user_id = message.from_user.id
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧨 Удалить профиль", callback_data="reset_confirm")]
    ])
    await message.answer("⚠️ Ты уверен, что хочешь удалить профиль и начать заново?", reply_markup=kb)

@router.callback_query(F.data == "reset_confirm")
async def reset_confirmed(call: types.CallbackQuery):
    user_id = call.from_user.id
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM user_profile WHERE user_id = ?", (user_id,))
        cur.execute("DELETE FROM weight_history WHERE user_id = ?", (user_id,))
        conn.commit()

    await call.message.answer("✅ Профиль удалён. Запусти /wizard чтобы создать новый.")
    await call.answer()
