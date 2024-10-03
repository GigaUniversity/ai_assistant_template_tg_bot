from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from source.config import Config
from source.handlers import user_router


# Инициализация объектов Диспетчера и Бота.
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN, 
          default=default_properties)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_router)