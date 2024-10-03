from source.bot import bot
from source.config import Config
from source.utils.logger_settings import logger
from source.utils import files_interactions



async def on_startup():
    """
    Функция, срабатывающая при запуске бота.
    Происходит подгрузка настроек, установка команд.
    Скачивается и сохраняется информация по университету.
    Сообщается Админу, что бот запущен.
    """
    settings = await files_interactions.json_loads(json_path=Config.SETTING_PATH)
    commands = settings.get('commands_for_bot')
    await bot.set_my_commands(commands=commands)
    
    status, json_data = await files_interactions.download_uni_info()
    if status == 200:
        is_downloaded = "Success download uni info"
        logger.info(is_downloaded)
    else:
        is_downloaded = "Failed download uni info"
        logger.warning(is_downloaded + ". Response: " + str(json_data))
    
    bot_info = await bot.get_me()
    text = 'Bot is started'
    text += "\n\n" + is_downloaded
    logger.info(f'Bot "{bot_info.username}" is started')
    await bot.send_message(chat_id=Config.ADMIN_ID,
                           text=text)


async def on_shutdown():
    """
    Функция, срабатывающая при выключении бота.
    Сообщается Админу, что бот остановлен.
    """
    bot_info = await bot.get_me()
    text = 'Bot is shutdown'
    logger.info(f'Bot "{bot_info.username}" is shutdown')
    await bot.send_message(chat_id=Config.ADMIN_ID,
                           text=text)
