from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from source.messages import messages
from source.keyboards import keyboards
from source.config import Config
from source.utils import files_interactions

# Здесь лежат все обработчики комманд (за исключением /start)

router = Router(name='user_commands_router')
    
@router.message(Command('take_the_survey'))
async def command_styles(message: Message, bot: Bot):
    """
    Команда для выдачи ссылки на прохождение опроса
    """
    settings = await files_interactions.json_loads(json_path=Config.SETTING_PATH)
    url = settings.get('link_to_feedback')
    await bot.send_message(chat_id=message.chat.id, text=messages.please_take_the_survey(url=url))
