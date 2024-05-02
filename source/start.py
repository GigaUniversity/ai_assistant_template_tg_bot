import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from source.config import Config
from source.handlers.user_handler import router
from source.utils.logger_settings import logger

default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=Config.bot_token, default=default_properties)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def on_startup_echo():
    text = 'Bot is started'
    logger.info(f'Bot for UNI "{Config.name_of_uni}" is started')
    await bot.send_message(chat_id=Config.admin_id,
                           text=text)


async def on_shutdown_echo():
    text = 'Bot is shutdown'
    logger.info(f'Bot for UNI "{Config.name_of_uni}" is shutdown')
    await bot.send_message(chat_id=Config.admin_id,
                           text=text)


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        dp.startup.register(on_startup_echo)
        dp.shutdown.register(on_shutdown_echo)
        await asyncio.gather(dp.start_polling(bot))
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
