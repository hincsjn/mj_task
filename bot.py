import asyncio
import logging

# from keyboards.keyboards import *
from handlers import system_handlers, chat_gpt_handlers, img_mj_handlers, translation_handlers, pay_handlers
from utils.system_utils import dp, bot
from aiogram.fsm.storage.redis import RedisStorage

from aiogram import Router
from aiogram.types import Message
from keyboards.keyboards import *
from all_states.states import BotStates
from messages.system_messages import *
from utils.system_utils import dp, bot
from messages.subsription_messages import *
from utils.system_utils import *

# from typing import Callable, Dict, Any, Awaitable
# from aiogram import BaseMiddleware
# from aiogram.types import TelegramObject

router = Router()


# class IfSubscriptionIsValid(BaseMiddleware):
#     # def __init__(self):
#     #     BaseMiddleware.__init__(self)

#     # async def check_users_subscription(self, message: Message):
#     #     print('============', message.text, message.from_user.id)
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any]
#     ):
#         await event.answer(
#             "Бот по выходным не работает!",
#             show_alert=True
#         )
#         print('============================')
#         result = await handler(event, data)
#         print(result)
#         # print('============================')

# router.message.middleware(IfSubscriptionIsValid())

@router.message(BotStates.menu)
async def mode_chosen_incorrectly(message: Message):
    user_id = message.from_user.id
    await message.answer(
        text="Я не знаю такой режим.\n\n"
             "Пожалуйста, выберите один из режимов из пункта выше:",
        reply_markup=make_menu_keyboard(user_id)   
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    

    # dp.middleware.setup(IfSubscriptionIsValid())
    # dp..outer_middleware(IfSubscriptionIsValid())
    dp.include_router(system_handlers.router)
    dp.include_router(chat_gpt_handlers.router)
    dp.include_router(translation_handlers.router)
    dp.include_router(img_mj_handlers.router)
    dp.include_router(pay_handlers.router)
    dp.include_router(router)


    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())


