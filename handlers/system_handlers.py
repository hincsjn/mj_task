from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.input_file import FSInputFile
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.filters.text import Text
from aiogram.filters import Text

import asyncio
from datetime import datetime
import json
import time

from utils import database, system_utils, update_gs
from keyboards.keyboards import *
from all_states.states import BotStates
from messages.system_messages import *
from messages.subsription_messages import *

from utils.system_utils import dp, bot


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    user_id = message.from_user.id
    # Рефералка
    referrer_id = message.text[7:]
    if referrer_id == "" or referrer_id == user_id:
        referrer_id = None
    elif not (database.check_if_user_exists(user_id)):
        referrer_id = int(referrer_id)
        referrals = database.get_user_attribute(referrer_id, 'referrals')
        referrals.append({'user_id': user_id, 'level': 1})
        database.set_user_attribute(referrer_id, 'referrals', referrals)

    # Регистрация
    await system_utils.register_user_if_not_exists(message, referrer_id)

    database.set_user_attribute(user_id, 'last_interaction', datetime.timestamp(datetime.now())*1000)

    # Приветствие
    await bot.send_message(chat_id=message.from_user.id,
                        text=greeting_msg,
                        parse_mode="MarkdownV2")
    
    # ПРОВЕРКА ТАРИФА ТУТ
    await asyncio.sleep(7)
    status = database.check_users_subscription(user_id)
    status, balance_in_seconds = status[0], status[1]
    print(balance_in_seconds)
    print(balance_in_seconds is float)
    print(balance_in_seconds < 0)
    if isfloat(balance_in_seconds) and balance_in_seconds < 0:
        status = 'У вас закончился тариф, перейдите в раздел "Оплата" для продления'
    
    await bot.send_message(chat_id=message.from_user.id,
                        text=status,
                        parse_mode='MarkdownV2',
                        reply_markup=make_mj_keyboard())
    if 'впервые' in status:
        await asyncio.sleep(8)
    else:
        await asyncio.sleep(5)

    await state.set_state(BotStates.menu)
    database.set_user_attribute(user_id, 'state', 'menu')
    await menu(message, state)
    

@router.message(
    F.text.in_([menu_button])
)
async def menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    print('MENU')
    await bot.send_message(chat_id=message.from_user.id,
                        text=make_menu_message(user_id),
                        parse_mode='MarkdownV2',
                        reply_markup=make_menu_keyboard(user_id),
                        disable_web_page_preview=True)
    await state.set_state(BotStates.menu)


@router.message(
    F.text.in_([referal_button])
)
async def referral_system(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id,
                        text=make_referral_info_msg(user_id),
                        parse_mode='MarkdownV2',
                        reply_markup=make_mj_keyboard(),
                        disable_web_page_preview=True)

    await state.set_state(BotStates.menu)


@router.message(Command("delete_me"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in [274370337, 248061526, 267313257]:
        with open(database_path, 'r', encoding='UTF-8')as f:
            database = json.load(f)

        for user in database:
            if user['id'] == user_id:
                database.remove(user)    

        with open(database_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False)
        
        await bot.send_message(chat_id=message.from_user.id,
                            text='Успешно',
                            parse_mode="MarkdownV2",
                            reply_markup=make_full_menu_keybord())


@router.message(Command("delete_all"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in [274370337, 248061526, 267313257]:
    
        with open(database_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)
        
        await bot.send_message(chat_id=message.from_user.id,
                            text='Успешно',
                            parse_mode="MarkdownV2",
                            reply_markup=make_full_menu_keybord())


@router.message(Command("mail_test"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in [274370337, 248061526, 267313257]:
        print('начали тестовую рассылку')
        print(message)
        if message.caption:
            post = message.caption.split('/mail_test')[1]
            photo = message.photo[-1]
            for user_id in test_mail_list:
                print(f'отправили -- {user_id}')
                await bot.send_photo(chat_id=str(user_id), photo=photo.file_id, caption=post, parse_mode='MarkdownV2')
        else:
            post = message.text.split('/mail_test')[1]

            for user_id in test_mail_list:
                try:
                    print(f'отправили -- {user_id}')
                    await bot.send_message(chat_id=str(user_id), text=post, parse_mode='MarkdownV2')
                except:
                    print(f'не отправили -- {user_id}')


@router.message(Command("mail_all"))
async def admin_mail_all_handle(message: Message):
    user_id = message.from_user.id
    if user_id in [274370337, 248061526, 267313257]:
        print('начали тестовую рассылку')
        print(message)
        if message.caption:
            post = message.caption.split('/mail_all')[1]

            photo = message.photo[-1]
            for user_id in update_gs.get_users():
                print(f'отправили -- {user_id}')
                await bot.send_photo(chat_id=str(user_id), photo=photo.file_id, caption=post, parse_mode='MarkdownV2')
        else:
            post = message.text.split('/mail_all')[1]

            for user_id in update_gs.get_users():
                try:
                    print(f'отправили -- {user_id}')
                    await bot.send_message(chat_id=str(user_id), text=post, parse_mode='MarkdownV2')
                except:
                    print(f'не отправили -- {user_id}')


@router.message(Command("update_gs"))
async def update_gs_handle(message: Message):
    print('update_gs')
    user_id = message.from_user.id
    if user_id in [274370337, 248061526, 267313257]: 
        update_gs.update_gs()
        await bot.send_message(chat_id=message.from_user.id,
                            text='Успешно обновил данные',
                            parse_mode="MarkdownV2",
                            reply_markup=make_full_menu_keybord())


@router.message(
    F.text.in_([support_button])
)
async def mode_chosen_incorrectly(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(chat_id=message.from_user.id,
                        text=support_msg,
                        parse_mode='MarkdownV2',
                        reply_markup=make_menu_keyboard(user_id))
    await state.set_state(BotStates.menu)
    

@router.message(
    BotStates.menu,
    ~(Text(text=menu_buttons))
)
async def invalid_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    print('MENU')
    await bot.send_message(chat_id=message.from_user.id,
                        text='Выберите режим работы из списка, пожалуйста',
                        parse_mode='MarkdownV2',
                        reply_markup=make_menu_keyboard(user_id))
    await state.set_state(BotStates.menu)
