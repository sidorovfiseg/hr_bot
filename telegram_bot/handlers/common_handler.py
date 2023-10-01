from aiogram import types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
import os
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot.states.user_state import UserState
from telegram_bot.routers.default_routers import default_router as router
from telegram_bot.keyboards.restart import restart_kb 
from telegram_bot.keyboards.cancel_generation import cg_kb
from telegram_bot.keyboards.menu import menu_kb
from telegram_bot.keyboards.get_back import return_kb 
from ml.answer import get_c
from telegram_bot.utils.split import split_text
import telegram_bot.callbacks.default_callbacks



# Обработка команды старта бота

@router.message(Command("start"))
async def start_bot(msg: Message, state: FSMContext):
    await state.set_state(UserState.menu_state)
    await msg.answer(text="Привет 🖐️. Ты можешь помочь мне обучением, добавив свой файл, или я могу ответить на интересующий тебя вопрос", \
        reply_markup=menu_kb)
    


# отрисовка меню     

@router.message(UserState.menu_state)
async def handle_menu(msg: Message, state: FSMContext):
    await state.set_state(UserState.menu_state)
    await msg.answer(text="Привет 🖐️. Ты можешь помочь мне обучением, добавив свой файл, или я могу ответить на интересующий тебя вопрос", \
        reply_markup=menu_kb)



# Переход из состояния старта в состояние ввода пользователем команды

@router.message(UserState.start_state)
async def handle_start_button(msg: Message, state: FSMContext):
    await msg.answer(text="Задайте вопрос, я помогу на него ответить 🧐")
    await state.set_state(UserState.answer_state)

    
# Отправка ответа на запрос пользователя

@router.message(UserState.answer_state, F.text)
async def generate_answer(msg: Message, state: FSMContext):
    
    ans = get_c(msg.text) 
    ans.replace("</s>", "").replace("<s>", "").replace("</unk>", "").replace("<unk>", "").\
            replace("</n>", "").replace("<n>", "")
    splitted_text = split_text(ans)
    
    await state.set_state(UserState.start_state)
    
    gen_msg = await msg.answer(
        "Подождите немного, я генерирую ответ... 🕐"
    )
    
    await gen_msg.edit_text(f"<h1>Ответ: <h1>")
    for i in range(len(splitted_text)):
        await msg.answer(f"{splitted_text[i]}")
    
    await msg.answer("Нажмите на кнопку, чтобы начать заново или попробуйте задать похожий вопрос", reply_markup=restart_kb)



# Обработка отправки файла

@router.message(UserState.download_state, F.document)
async def handle_file(msg: Message, state: FSMContext):
    file_id_doc = msg.document.file_id
    file = await msg.bot.get_file(file_id_doc)
    file_path = file.file_path
    local_path = f"./data/{msg.document.file_name}"
    
    if os.path.exists(local_path) == False:
        await msg.bot.download_file(file_path, local_path)
        await msg.answer("Добавила, вернитесь в меню или продолжайте... 👉🏻👈🏻", reply_markup=return_kb)
    else:
        await msg.answer("Упс, такой файл уже существует, попробуйте добавить другой файл",
                         reply_markup=return_kb)
    