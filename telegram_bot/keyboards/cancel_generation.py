from aiogram import types

cancel_generation = [
    [
        types.InlineKeyboardButton(text="Отменить генерацию ❌",
                                   callback_data="cancel")
    ]
]

cg_kb = types.InlineKeyboardMarkup(
    inline_keyboard=cancel_generation
)