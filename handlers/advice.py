from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.openai_advisor import ask_openai

router = Router()

class AdviceStates(StatesGroup):
    awaiting_question = State()

@router.message(Command("advice"))
async def advice_handler(message: types.Message, state: FSMContext):
    await message.answer("✍️ Задай свой вопрос (например: 'Что делать, если вес стоит?' или 'Придумай меню на день без мяса'):")
    await state.set_state(AdviceStates.awaiting_question)

@router.message(AdviceStates.awaiting_question)
async def advice_answer(message: types.Message, state: FSMContext):
    question = message.text.strip()
    await message.answer("🤔 Думаю над ответом...")
    answer = ask_openai(question)
    await message.answer(f"💡 {answer}")
    await state.clear()
