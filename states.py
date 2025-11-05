from aiogram.fsm.state import State,StatesGroup

class Sign_up(StatesGroup):
    name = State()
    age = State()