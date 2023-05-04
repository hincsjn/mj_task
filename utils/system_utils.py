from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from datetime import datetime

from static.config import telegram_token
from utils import database

bot = Bot(telegram_token)
storage = RedisStorage.from_url('redis://default:123@0.0.0.0:6379')
dp = Dispatcher(bot=bot, storage=storage)
async def register_user_if_not_exists(message: Message, referrer_id=None):
    
    user = message.from_user
    if not (database.check_if_user_exists(user.id)):
        database.add_new_user(
            user.id,
            user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            referrer_id=referrer_id
        )
        database.start_new_dialog(user.id)

    if database.get_user_attribute(user.id, "current_dialog_id") is None:
        database.start_new_dialog(user.id)

    if database.get_user_attribute(user.id, "current_chat_mode") is None:
        database.set_user_attribute(user.id, 'current_chat_mode', 'assistant')

