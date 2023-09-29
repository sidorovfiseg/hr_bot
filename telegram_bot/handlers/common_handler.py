from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F

router = Router()

@router.message(Command("start"))
async def start_bot(msg: Message):
    await msg.answer("Привет, пора начинать работать!")

