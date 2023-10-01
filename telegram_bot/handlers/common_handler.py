from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from io import BytesIO
from telegram_bot.config.config_reader import config
import os
from aiogram.utils.keyboard import InlineKeyboardBuilder
from ml.answer import get_answer

router = Router()


class UserState(StatesGroup):
    start_state = State()
    answer_state = State()


@router.message(Command("start"))
async def start_bot(msg: Message, state: FSMContext):
    await msg.answer(text="Введите ваш вопрос ❤️")
    await state.set_state(UserState.answer_state)


@router.callback_query(F.data == "start")
async def handle_start_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ваш вопрос ❤️")
    await state.set_state(UserState.answer_state)
    await callback.answer()


@router.message(UserState.start_state)
async def handle_start_button(msg: Message, state: FSMContext):
    await msg.answer(text="Введите ваш вопрос ❤️")
    await state.set_state(UserState.answer_state)






def split_text(text: str, max_chars: int = 4096) -> list:
    result = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    return result


@router.message(UserState.answer_state, F.text)
async def generate_answer(msg: Message, state: FSMContext):
    ans = get_answer(msg.text)
    # ans = your_function(msg.text)
    await state.set_state(UserState.start_state)

    another_builder = InlineKeyboardBuilder()
    another_builder.add(types.InlineKeyboardButton(
        text="Начать заново",
        callback_data="start"
    ))
    ans = ans.\
        replace("</s>", "").replace("<s>", "").replace("</unk>", "").replace("<unk>", "").\
            replace("</n>", "").replace("<n>", "")
    splitted_text = split_text(ans)

    for i in range(len(splitted_text)):
        await msg.answer(f"{splitted_text[i]}")

    await msg.answer("Нажмите на кнопку, чтобы начать заново", reply_markup=another_builder.as_markup())


@router.message(F.document)
async def handle_file(msg: Message):
    file_id_doc = msg.document.file_id
    file = await msg.bot.get_file(file_id_doc)
    file_path = file.file_path
    local_path = f"./data/{msg.document.file_name}"

    if os.path.exists(local_path) == False:
        await msg.bot.download_file(file_path, local_path)
