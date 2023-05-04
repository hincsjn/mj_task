from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.buttons import *
from utils import database


def make_menu_keyboard(user_id) -> ReplyKeyboardMarkup:
    sub_name = database.get_user_attribute(user_id, 'subscription')['name']
    print(f'------ {sub_name}')
    if sub_name == 'Midjourney':
        return make_mj_menu_keyboard()
    elif sub_name == 'ChatGPT':
        return make_chat_gpt_menu_keyboard()
    else:
        return make_full_menu_keybord()


def make_mj_menu_keyboard():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [state2img_mj_button, support_button]])
    keyboard.append([KeyboardButton(text=item) for item in [pay_button, referal_button]])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_mj_keyboard():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [menu_button]])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_mj_pro_instructure_keyboard():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [pro_instructue_mj_button]])
    keyboard.append([KeyboardButton(text=item) for item in [menu_button]])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_chat_gpt_menu_keyboard():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [state2chat_gpt_button, state2translation_button]])
    keyboard.append([KeyboardButton(text=item) for item in [support_button, pay_button]])
    keyboard.append([KeyboardButton(text=item) for item in [referal_button]])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_chat_gpt_instruction_keyboard():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [instructure_button]])
    keyboard.append([KeyboardButton(text=item) for item in [menu_button]])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_chat_mj_instruction_keyboard():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [instructure_button]])
    keyboard.append([KeyboardButton(text=item) for item in [menu_button]])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_chat_gpt_keyboard():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [retry_button, delete_dialog]])
    keyboard.append([KeyboardButton(text=item) for item in [instructure_button, menu_button]])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_full_menu_keybord():
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [state2chat_gpt_button, state2img_mj_button]])
    keyboard.append([KeyboardButton(text=item) for item in [state2translation_button, support_button]])

    keyboard.append([KeyboardButton(text=item) for item in [pay_button, referal_button]])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def chose_lang_keyboard() -> ReplyKeyboardMarkup:
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [rus_button, eng_button]])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def translation_keyboard() -> ReplyKeyboardMarkup:
    keyboard = []
    keyboard.append([KeyboardButton(text=item) for item in [change_language]])
    keyboard.append([KeyboardButton(text=item) for item in [menu_button]])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def make_img_variations_remake_inline_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [ub1, ub2, ub3, ub4, rb1],
        [vb1, vb2, vb3, vb4]
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return ikb
    

def make_tariffs_inline_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text=sub_chat_gpt_standart_name, callback_data=sub_chat_gpt_standart_name), 
            InlineKeyboardButton(text=sub_img_mj_standart_name, callback_data=sub_img_mj_standart_name)
         ],
        [   
            InlineKeyboardButton(text=sub_all_standart_name, callback_data='ChatGPT_and_Midjourney')
        ]
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return ikb


def make_sub_duration_inline_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text=month_sub, callback_data='month'), 
            InlineKeyboardButton(text=week_sub, callback_data='week')
         ],
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return ikb


def make_new_shit():
    buttons = [
        [
            InlineKeyboardButton(text=sub_chat_gpt_standart_name, callback_data=sub_chat_gpt_standart_name), 
            InlineKeyboardButton(text=sub_img_mj_standart_name, callback_data=sub_img_mj_standart_name)
         ],
        [   
            InlineKeyboardButton(text=sub_all_standart_name, callback_data='ChatGPT_and_Midjourney')
        ],
        [
            InlineKeyboardButton(text='О подписке', callback_data='О подписке'), 
            InlineKeyboardButton(text='Отписка', callback_data='Отписка')
         ],
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return ikb


def decline_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text='Да', callback_data='Да'), 
            InlineKeyboardButton(text='Нет', callback_data='нет')
         ],
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return ikb
