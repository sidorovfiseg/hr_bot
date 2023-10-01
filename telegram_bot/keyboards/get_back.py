from aiogram import types

return_menu = [
    [
        types.InlineKeyboardButton(text="Вернуться в меню ⤴️",
                                   callback_data="return")
    ], 
]

return_kb = types.InlineKeyboardMarkup(
    inline_keyboard=return_menu
)