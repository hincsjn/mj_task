from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardButton
from static.config import *


ub1 = InlineKeyboardButton(text='U1', callback_data='U1')
ub2 = InlineKeyboardButton(text='U2', callback_data='U2')
ub3 = InlineKeyboardButton(text='U3', callback_data='U3')
ub4 = InlineKeyboardButton(text='U4', callback_data='U4')

vb1 = InlineKeyboardButton(text='V1', callback_data='V1')
vb2 = InlineKeyboardButton(text='V2', callback_data='V2')
vb3 = InlineKeyboardButton(text='V3', callback_data='V3')
vb4 = InlineKeyboardButton(text='V4', callback_data='V4')

rb1 = InlineKeyboardButton(text='🔄', callback_data='🔄')

process_img_mj_buttons = ['U1', 'U2', 'U3', 'U4', 'V1', 'V2', 'V3', 'V4', '🔄']


menu_button = '⤴️Меню'
state2chat_gpt_button = '📝Режим: Текст'
retry_button = '🔄Повторить'
delete_dialog = '🗑Очистить историю'
state2img_mj_button = '🖼Режим: Графика'
state2translation_button = '🌎Переводчик'
change_language = '🌎Изменить язык'
instructure_button = '📋Инструкция'
pro_instructue_mj_button = 'ДЛЯ PRO👨‍💻'
pay_button = '💰Оплата'
rus_button = 'Русский 🇷🇺'
eng_button = 'Английский 🇬🇧'


support_button = '👨‍🚀Поддержка'
referal_button = '🤝Партнерка'

menu_buttons = [
    state2chat_gpt_button,
    state2img_mj_button,
    state2translation_button,
    instructure_button,
    menu_button,
    pay_button,
    referal_button,
    support_button
    ]

week_sub = '1 неделя'
month_sub = '1 месяц'


sub_chat_gpt_standart_name = f'ChatGPT'
sub_img_mj_standart_name = f'Midjourney'
sub_all_standart_name = f'Все включено'

sub_chat_gpt_standart = f'Оплата подписки "{sub_chat_gpt_standart_name}"'
sub_img_mj_standart = f'Оплата подписки "{sub_img_mj_standart_name}"'
sub_all_standart = f'Оплата подписки "{sub_all_standart_name}"'


all_buttons = [
    state2chat_gpt_button, 
    retry_button, 
    state2translation_button,
    state2img_mj_button,
    rus_button,
    eng_button,
    support_button,
    referal_button,
    pay_button,
    delete_dialog,
    change_language,
    week_sub,
    month_sub,
    menu_button,
    pro_instructue_mj_button,
    instructure_button,
    '/start',
    'Меню'
]