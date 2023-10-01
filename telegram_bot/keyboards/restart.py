from aiogram import types

restart = [
    [
        types.InlineKeyboardButton(text="Задать новый вопрос 🔄️",
                                   callback_data="restart")
    ], 
    [
        types.InlineKeyboardButton(text="Вернуться в меню ⤴️",
                                   callback_data="return")
    ], 
]

restart_kb = types.InlineKeyboardMarkup(
    inline_keyboard=restart
)