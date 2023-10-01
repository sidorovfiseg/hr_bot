from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


# Установка команд пользователя

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы 🤖'
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())