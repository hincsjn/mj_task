from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.handlers import CallbackQueryHandler
from aiogram.types.input_file import FSInputFile
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.filters.text import Text
from aiogram.filters import Text

from datetime import datetime
import glob
import os
import requests
import asyncio


from keyboards.keyboards import *
from all_states.states import BotStates
from messages.img_mj_messages import *
from keyboards.buttons import *
from static.config import stop_word_list_path
from utils.system_utils import *
from utils import img_mj_utils
from utils.translate_utils import translate


router = Router()

@router.message(
    F.text.in_([state2img_mj_button])
)
async def img_mj_chosen(message: Message, state: FSMContext):
    await register_user_if_not_exists(message)
    mode = message.text
    await state.update_data(mode=mode)
    await message.answer(
        text=img_mj_start_message,
        reply_markup=make_chat_mj_instruction_keyboard(),
        parse_mode='MarkdownV2'
    )
    await state.set_state(BotStates.img_mj)


@router.message(
    BotStates.img_mj,
    F.text.in_([instructure_button])
)
async def instructure(message: Message, state: FSMContext):
    await register_user_if_not_exists(message)
    mode = message.text
    await state.update_data(mode=mode)
    await bot.send_message(chat_id=message.from_user.id,
                        text=img_mj_instruction_message,
                        parse_mode="MarkdownV2",
                        reply_markup=make_mj_pro_instructure_keyboard(),
                        disable_web_page_preview=True)
    await state.set_state(BotStates.img_mj)


@router.message(
    BotStates.img_mj,
    F.text.in_([pro_instructue_mj_button])
)
async def pro_instructure(message: Message, state: FSMContext):
    await register_user_if_not_exists(message)
    mode = message.text
    await state.update_data(mode=mode)
    await bot.send_message(chat_id=message.from_user.id,
                        text=img_mj_instruction4pro,
                        parse_mode="MarkdownV2",
                        reply_markup=make_mj_keyboard(),
                        disable_web_page_preview=True)
    await state.set_state(BotStates.img_mj)


@router.message(
    BotStates.img_mj,
    ~(F.text.in_(all_buttons))
)
async def img_mj(message: Message):
    await register_user_if_not_exists(message)
    def check_violation(prompt):
        my_file = open(stop_word_list_path, "r")
        
        data = my_file.read()
        data_into_list = data.replace('\n', '$').split("$")
        my_file.close()
        prompt = prompt.split(' ')
        for word in prompt:
            for stop_word in data_into_list:
                if word.lower() == stop_word.lower() and stop_word != '':
                    print(word, stop_word)
                    return 'violation', stop_word
        
        prompt = " ".join(prompt)
        return prompt, ''
    
    def check_not_russian(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        return alphabet.isdisjoint(text.lower())

    user_id = message.from_user.id
    prompt = message.text

    print(f'MJ-User {user_id}: {prompt}')
    database.set_user_attribute(user_id, "last_interaction", datetime.timestamp(datetime.now())*1000)
    if not(check_not_russian(prompt)):
        answer = await translate(
            prompt,
            dialog_messages=[],
            chat_mode='any-eng', 
            lang='eng'
        )
        prompt = answer[0]
        n_used_tokens = answer[1]
        database.set_user_attribute(user_id, "n_used_tokens", n_used_tokens + database.get_user_attribute(user_id, "n_used_tokens"))

        while '"' in prompt:
            prompt = prompt.replace('"', '')
        
        while 'in english' in prompt.lower():
            prompt = prompt.lower().replace('in english', '')

        while '.' in prompt:
            prompt = prompt.replace('.', '')

    current_status = database.get_img_attribute('user_id', user_id, 'status')
    last_img_request_time = database.get_img_attribute('user_id', user_id, 'time')
    
    if (current_status == 'just_got' and datetime.timestamp(datetime.now())*1000 - last_img_request_time < 10000) or (current_status == 'request sent' and datetime.timestamp(datetime.now())*1000 - last_img_request_time < 300000):
        await bot.send_message(chat_id=message.from_user.id,
                        text=wait_msg,
                        parse_mode="HTML",
                        reply_markup=make_mj_keyboard())
        return

    while '\n' in prompt:
        prompt = prompt.replace('\n', ' ')

    while '—' in prompt:
        prompt = prompt.replace('—', '--')

    while '-->' in prompt:
        prompt = prompt.split('-->')[0]

    while '->' in prompt:
        prompt = prompt.split('->')[0]

    if not('--v 5' in prompt):
        prompt = prompt + ' --v 5'

    prompt = prompt.split()
    prompt = " ".join(prompt)
    

    prompt, stop_word = check_violation(prompt)

    if prompt == 'violation':
        await bot.send_message(chat_id=user_id,
                        text=f"Нарушение правил midjourney!\nИзмените запрос, исключите слово {stop_word}",
                        parse_mode='HTML',
                        reply_markup=make_mj_keyboard())
        return
    
    res = img_mj_utils.send_response_midjourney(prompt)

    if not(res):
        return
        
    database.set_img_attribute('user_id', user_id, 'prompt', prompt)
    database.set_img_attribute('user_id', user_id, 'status', 'just_got')
    database.set_img_attribute('user_id', user_id, 'time', datetime.timestamp(datetime.now())*1000)


async def download_img(user_id, url, ds_msg_url, mode):
    filename = url.split('_')[-1].split('.')[0]
    print(filename)
    message_id = ds_msg_url
    print(message_id)

    # if '- Upscaled by' in message.content or '- Image #' in message.content:
    #     mode = 'U'
    # elif '- Variations by' in message.content:
    #     mode = 'V'
    # else:
    
    print('try to download ----', url, f"{filename}", user_id, message_id, mode)
    directory = os.getcwd()
    
    print(f'filename -- {filename}')
    user_id = int(user_id)
    response = requests.get(url)
    if response.status_code == 200:
        input_folder = "input"
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)

        with open(f"{directory}/{input_folder}/{filename}", "wb") as f:
            f.write(response.content)
        print(f"Image downloaded: {filename}")
    
        await send_mj_image(user_id, input_folder, filename, message_id, mode)


async def send_mj_status(prompt, msg, status):
    print(f'================{status}================')
    user_id = database.get_img_attribute('prompt', prompt, 'user_id')
    print(f'userid {user_id}')
    if user_id:
        database.set_img_attribute('user_id', user_id, 'status', status)
        database.set_img_attribute('user_id', user_id, 'time', datetime.timestamp(datetime.now())*1000)

        if status == 'request sent':
            must_delete = await bot.send_message(chat_id=user_id,
                                                text=msg,
                                                parse_mode='HTML')
                                                # reply_markup=make_mj_keyboard())
        
            must_delete_id = must_delete.message_id
            database.set_img_attribute('user_id', user_id, 'must_delete', must_delete_id)

        if status == 'loading':
            try:
                must_delete_id = database.get_img_attribute('user_id', user_id, 'must_delete')
                # await must_delete_id.delete_message(user_id, must_delete_id)
                await bot.edit_message_text(msg, user_id, must_delete_id)
            except:
                must_delete = await bot.send_message(chat_id=user_id,
                                                    text=msg,
                                                    parse_mode='HTML')
                
                must_delete_id = must_delete.message_id
            
                database.set_img_attribute('user_id', user_id, 'must_delete', must_delete_id)
        if 'response got' in status:
            print('------------------')
            img_url = msg.split(' | ')[0]
            ds_msg_url = msg.split(' | ')[-1]
            if 'upscaled' in status:
                await download_img(user_id, img_url, ds_msg_url, mode='U')
            else:
                await download_img(user_id, img_url, ds_msg_url, mode=None)
        elif status == 'error':
            await bot.send_message(chat_id=user_id,
                                text=msg,
                                parse_mode='HTML')


async def send_mj_image(user_id, file_path, filename, ds_message_id, mode):
    prompt = database.get_img_attribute('user_id', user_id, 'prompt')
    photo = FSInputFile(f'{file_path}/{filename}')
    print(f'MODE -- {mode}')
    if mode == 'U':
        file_id = await bot.send_photo(chat_id=str(user_id), photo=photo, caption=prompt, parse_mode='HTML')
        await bot.send_message(chat_id=user_id,
                            text=img_done,
                            parse_mode="HTML",
                            reply_markup=make_chat_mj_instruction_keyboard())
    elif mode in ['V', '🔄', None]:
        file_id = await bot.send_photo(chat_id=str(user_id), photo=photo, caption=prompt, parse_mode='HTML', reply_markup=make_img_variations_remake_inline_keyboard())
        await bot.send_message(chat_id=user_id,
                            text=img_done,
                            parse_mode="HTML",
                            reply_markup=make_chat_mj_instruction_keyboard())
        
    file_id = dict(dict(file_id)['photo'][0])['file_id']

    database.set_img_id_attribute(file_id, filename, ds_message_id)
    
    database.set_img_attribute('user_id', user_id, 'status', 'successfully_sent_to_tg')
    database.set_img_attribute('user_id', user_id, 'time', datetime.timestamp(datetime.now())*1000)
    
    must_delete_id = database.get_img_attribute('user_id', user_id, 'must_delete')
    await bot.delete_message(user_id, must_delete_id)

    removing_files = glob.glob(f'{file_path}/{filename}*')
    for file in removing_files:
        os.remove(file)
    database.delete_last_prompt(user_id)


# @router.message(
#     # BotStates.img_mj,
#     F.text.in_(process_img_mj_buttons),
#     # ~(F.text.in_(all_buttons))
#     ~(F.text.in_([week_sub, month_sub]))
# )
@router.callback_query(
    Text(text=process_img_mj_buttons)
    )
async def process_photo_callback(callback: CallbackQuery):
    print('-----------', F.text.text)
    prompt = callback.message.caption
    tg_photo_id = callback.message.photo[0].file_id
    user_id = callback.from_user.id

    print(f'Получили callback {prompt} {callback.data} от {user_id}, tg_photo_id: {tg_photo_id}')
    
    database.set_user_attribute(user_id, "last_interaction", datetime.timestamp(datetime.now())*1000)
    current_status = database.get_img_attribute('user_id', user_id, 'status')

    try:
        last_img_request_time = database.get_img_attribute('user_id', user_id, 'time')

        if (current_status == 'just_got' and datetime.timestamp(datetime.now())*1000 - last_img_request_time < 10000) or (current_status == 'sent_to_mj' and datetime.timestamp(datetime.now())*1000 - last_img_request_time < 300000):
            await bot.send_message(chat_id=user_id,
                            text='Пожалуйста, дождитесь ответа на прошлый запрос',
                            parse_mode="HTML",
                            reply_markup=make_mj_keyboard())
            await callback.answer()
            return
    
    except:
        ...
    

    do = request_accepted

    if 'U' in callback.data:
        do = '⏳ Upscale '+callback.data[-1]
        img_mj_utils.process_mj_imj('upsample', tg_photo_id, list(callback.data)[-1])
    elif 'V' in callback.data:
        do = '⏳ Variations '+callback.data[-1]
        img_mj_utils.process_mj_imj('variation', tg_photo_id, list(callback.data)[-1])
    elif '🔄' in callback.data:
        do = '⏳ Remake'
        img_mj_utils.process_mj_imj('reroll', tg_photo_id, 0)

    must_delete = await bot.send_message(chat_id=user_id,
                        text=do,
                        parse_mode='HTML',
                        reply_markup=make_mj_keyboard())
    must_delete_id = dict(must_delete)['message_id']

    database.set_img_attribute('user_id', user_id, 'prompt', prompt)
    database.set_img_attribute('user_id', user_id, 'status', 'just_got')
    database.set_img_attribute('user_id', user_id, 'time', datetime.timestamp(datetime.now())*1000)
    database.set_img_attribute('user_id', user_id, 'must_delete', must_delete_id)

    await callback.answer()