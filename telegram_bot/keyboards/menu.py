from aiogram import types


menu = [
    [
        types.InlineKeyboardButton(
            text="Подгрузить в меня файлы 👉🏻👈🏻",
            callback_data="download_file"
        )
    ],
    [
        types.InlineKeyboardButton(
                text="Ответить на ваш вопрос 😊",
                callback_data="ask_question"
            )
    ]
]

menu_kb = types.InlineKeyboardMarkup(
    inline_keyboard=menu
)
