from aiogram.dispatcher.filters.state import StatesGroup, State

class NewEvent(StatesGroup):
    logo = State()
    desc_logo = State()
    date = State()
    time = State()
    