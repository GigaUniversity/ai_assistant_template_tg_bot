import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from source.config import Config
from source.handlers import user_router
from source.utils.logger_settings import logger
from source.utils import files_interactions

default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN, default=default_properties)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_router)


async def on_startup():
    settings = await files_interactions.json_loads(json_path=Config.SETTING_PATH)
    commands = settings.get('commands_for_bot')
    await bot.set_my_commands(commands=commands)
    
    status, json_data = await files_interactions.download_uni_info()
    if status == 200:
        is_downloaded = "Success download uni info"
        logger.info(is_downloaded)
    else:
        is_downloaded = "Failed download uni info :("
        logger.warning(is_downloaded + " Response: " + str(json_data))
    
    bot_info = await bot.get_me()
    text = 'Bot is started'
    text += "\n\n" + is_downloaded
    logger.info(f'Bot "{bot_info.username}" is started')
    await bot.send_message(chat_id=Config.ADMIN_ID,
                           text=text)


async def on_shutdown():
    bot_info = await bot.get_me()
    text = 'Bot is shutdown'
    logger.info(f'Bot "{bot_info.username}" is shutdown')
    await bot.send_message(chat_id=Config.ADMIN_ID,
                           text=text)


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await asyncio.gather(dp.start_polling(bot))
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
