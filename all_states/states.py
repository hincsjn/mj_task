from aiogram.fsm.state import StatesGroup, State

class BotStates(StatesGroup):
    menu = State()
    chat_gpt = State()
    img_mj = State()
    translation = State()
    chose_lang = State()
    pay = State()
    pay_week = State()
    pay_month = State()
    payed = State()

    choose_sub_duration = State()
