from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from io import BytesIO
from telegram_bot.config.config_reader import config
import os
router = Router()

@router.message(Command("start"))
async def start_bot(msg: Message):
    await msg.answer("Привет, пора начинать работать!")


@router.message(F.document)
async def handle_file(msg: Message):
    file_id_doc = msg.document.file_id
    file = await msg.bot.get_file(file_id_doc)
    file_path = file.file_path
    local_path = f"./data/{msg.document.file_name}"
    
    if os.path.exists(local_path) == False:
        await msg.bot.download_file(file_path, local_path)
    