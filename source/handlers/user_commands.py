from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from source.messages import messages
from source.keyboards import keyboards
from source.config import Config
from source.utils.logger_settings import logger
from source.utils import files_interactions

user_commands_router = Router(name='user_commands_router')


@user_commands_router.message(Command('styles'))
async def command_styles(message: Message, bot: Bot):
    """
    Обработчик команды по поводу смены стиля диалога
    """
    settings = await files_interactions.json_loads(json_path=Config.SETTING_PATH)
    styles_list = settings.get('styles_of_dialog')
    await bot.send_message(chat_id=message.chat.id, text=messages.choose_your_style(),
                           reply_markup=keyboards.choose_the_style(styles_list=styles_list))


@user_commands_router.callback_query(F.data.startswith("choose_the_style"))
async def choose_the_uni(call: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Выбор конкретного стиля диалога
    """
    _, dialog_style = call.data.split('|')
    name_of_dialog = call.message.reply_markup.inline_keyboard[0][0].text
    await state.update_data(dialog_style=dialog_style)
    await bot.send_message(chat_id=call.message.chat.id,
                           text=messages.success_choose_dialog_style(name_of_dialog))
    
    
@user_commands_router.message(Command('take_the_survey'))
async def command_styles(message: Message, bot: Bot):
    """
    Команда для выдачи ссылки на прохождение опроса
    """
    settings = await files_interactions.json_loads(json_path=Config.SETTING_PATH)
    url = settings.get('link_to_feedback')
    await bot.send_message(chat_id=message.chat.id, text=messages.please_take_the_survey(url=url))
