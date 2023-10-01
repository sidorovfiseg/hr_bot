from aiogram import types

restart = [
    [
        types.InlineKeyboardButton(text="Задать новый вопрос 🔄️",
                                   callback_data="restart")
    ], 
    [
        types.InlineKeyboardButton(text="Выбрать похожий вопрос ", 
                                   callback_data="similar_quest")
    ]
]

restart_kb = types.InlineKeyboardMarkup(
    inline_keyboard=restart
)