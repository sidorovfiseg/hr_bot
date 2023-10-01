from telegram_bot.routers.default_routers import default_router as router
from telegram_bot.states.user_state import UserState
from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.keyboards.menu import menu_kb



# Обработка похожих вопросов

@router.callback_query(F.data == "download_file", UserState.menu_state)
async def handle_download(callback : types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Отправьте файл для дообучения 📄")
    await state.set_state(UserState.download_state)
    await callback.answer()

@router.callback_query(F.data == "return")
async def handle_return(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.menu_state)
    await callback.message.answer(text="Привет 🖐️. Ты можешь помочь мне обучением, добавив свой файл, или я могу ответить на интересующий тебя вопрос", \
        reply_markup=menu_kb)
    await callback.answer()


@router.callback_query(F.data == "restart")
async def handle_new_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Задайте вопрос, я помогу на него ответить 🧐")
    await state.set_state(UserState.answer_state)
    await callback.answer()
  
    
# @router.callback_query(F.data == "similar_quest")
# async def handle_sim_questions(callback: types.CallbackQuery, state: FSMContext):
    
    # df_question = df['QUESTION'].to_list()

    # kb = [[types.KeyboardButton(text=question)] for question in df_question]
    # sq_kb = types.ReplyKeyboardMarkup(
    #         keyboard=kb,
    #         resize_keyboard=True,
    #         is_persistent=True,
    #         input_field_placeholder = "Похожие вопросы"
    #     )
    
    #await callback.message.answer(text="Выберите похожий вопрос или задайте свой", reply_markup=sq_kb)
    

    

@router.callback_query(F.data == "ask_question")
async def handle_ask_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Задайте вопрос, я помогу на него ответить 🧐")
    await state.set_state(UserState.answer_state)
    await callback.answer()