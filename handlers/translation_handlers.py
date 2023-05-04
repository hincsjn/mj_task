from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from datetime import datetime
import asyncio

from keyboards.keyboards import *
from all_states.states import BotStates
from messages.translation_messages import *
from keyboards.buttons import *
from utils.system_utils import *
from utils.translate_utils import translate


router = Router()


@router.message(
    F.text.in_([state2translation_button, change_language])
)
async def translation_chosen(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await register_user_if_not_exists(message)
    database.set_user_attribute(user_id, "last_interaction", datetime.timestamp(datetime.now())*1000)

    mode = message.text
    await state.update_data(mode=mode)
    await message.answer(
        text=translation_start_msg,
        reply_markup=chose_lang_keyboard()
    )
    await state.set_state(BotStates.chose_lang)


@router.message(
    BotStates.chose_lang, 
    F.text.in_([rus_button, eng_button])
)
async def lang_chosen(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await register_user_if_not_exists(message)
    database.set_user_attribute(user_id, "last_interaction", datetime.timestamp(datetime.now())*1000)
    if message.text == rus_button:
        database.set_user_attribute(user_id, 'lang', 'ru')
    elif message.text == eng_button:
        database.set_user_attribute(user_id, 'lang', 'eng')

    await message.answer(
        text=translation_after_language,
        reply_markup=translation_keyboard(),
        parse_mode='MarkdownV2'
    )
    await state.set_state(BotStates.translation)


@router.message(
    BotStates.chose_lang,
)
async def lang_chosen_incorrect(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await register_user_if_not_exists(message)
    database.set_user_attribute(user_id, "last_interaction", datetime.timestamp(datetime.now())*1000)

    await message.answer(
        text=lang_error,
        reply_markup=chose_lang_keyboard()
    )


@router.message(
    BotStates.translation,
    ~(F.text.in_(all_buttons))
)
async def lang_chosen(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await register_user_if_not_exists(message)
    database.set_user_attribute(user_id, "last_interaction", datetime.timestamp(datetime.now())*1000)

    lang = database.get_user_attribute(user_id, 'lang')

    if database.get_user_attribute(user_id, 'if_answered') == 'not_answered':
        await bot.send_message(chat_id=message.from_user.id,
                        text=not_now,
                        parse_mode="HTML",
                        reply_markup=translation_keyboard())
        return

    must_delete = await bot.send_message(chat_id=message.from_user.id,
                        text=wait_for_answer,
                        parse_mode="HTML",
                        reply_markup=translation_keyboard())

    # await message.answer_chat_action("typing")
    
    try:
        message = message.text
        print(f'got: {message}')
        chat_mode = database.get_user_attribute(user_id, "current_chat_mode")
        
        answer, n_used_tokens, n_first_dialog_messages_removed = await translate(
            message,
            dialog_messages=[],
            chat_mode=chat_mode, 
            lang=lang
        )

        database.set_user_attribute(user_id, "if_answered", 'answered')
        print(f'Bot {user_id}: {answer}')

        try:
            await must_delete.delete()
            await bot.send_message(chat_id=user_id,
                            text=answer,
                            parse_mode="HTML",
                            reply_markup=translation_keyboard())
            
        except Exception as e:
            print(e)
            await bot.send_message(chat_id=user_id,
                            text=error_msg,
                            parse_mode="HTML",
                            reply_markup=translation_keyboard())
        await asyncio.sleep(0.01)

        database.set_user_attribute(user_id, "n_used_tokens", n_used_tokens + database.get_user_attribute(user_id, "n_used_tokens"))

    except Exception as e:
        database.set_user_attribute(user_id, "if_answered", 'answered')
        print(e)
        await bot.send_message(chat_id=user_id,
                        text=error_msg,
                        parse_mode="HTML",
                        reply_markup=translation_keyboard())