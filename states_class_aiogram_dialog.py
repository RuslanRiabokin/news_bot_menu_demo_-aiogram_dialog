from aiogram.fsm.state import State, StatesGroup

class MainDialogSG(StatesGroup):
    start = State()
    menu = State()
    new_subscription = State()
    enter_news = State()

class SecondDialogSG(StatesGroup):
    first = State()
    second = State()

class EditSubscriptions(StatesGroup):
    select_language = State()
    edit = State()
