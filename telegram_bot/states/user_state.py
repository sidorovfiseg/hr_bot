from aiogram.fsm.state import StatesGroup, State

# Класс состояний

class UserState(StatesGroup):
    start_state = State()
    answer_state = State()
    download_state = State()
    menu_state = State()