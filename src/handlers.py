from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject

import service_messages
from config import Config as config

router = Router(name='main_router')


@router.message(CommandStart())
async def hello(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.chat.id, text=service_messages.hello_message())


@router.message()
async def take_query_from_user(message: Message, bot: Bot):
    metadata_of_query = {
        'query': message.text,
        'datetime': message.date,
        'chat_id': message.chat.id,
        'message_id': message.message_id,
        'gigachat_token': config.gigachat_token,
    }
