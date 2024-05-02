from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from source.messages import service_messages
from source.keyboards import keyboards
from source.config import Config
from source.utils.logger_settings import logger

user_commands_router = Router(name='user_commands_router')


@user_commands_router.message(CommandStart())
async def hello(message: Message, bot: Bot):
    logger.info(f'Пользователь {message.from_user.id} написал команду /start')
    await bot.send_message(chat_id=message.chat.id, text=service_messages.hello_message(name_of_uni=Config.name_of_uni))


@user_commands_router.message(Command('styles'))
async def command_styles(message: Message, bot: Bot):
    """
    Обработчик команды по поводу смены стиля диалога
    """
    await bot.send_message(chat_id=message.chat.id, text=service_messages.choose_your_style(),
                           reply_markup=keyboards.choose_the_style(styles_list=Config.styles_of_dialog))


@user_commands_router.callback_query(F.data.startswith("choose_the_style"))
async def choose_the_uni(bot: Bot, call: CallbackQuery, state: FSMContext):
    """
    Выбор конкретного стиля диалога
    """
    _, dialog_style = call.data.split('|')
    name_of_dialog = call.message.reply_markup.inline_keyboard[0][0].text
    await state.update_data(dialog_style=dialog_style)
    await bot.send_message(chat_id=call.message.chat.id,
                           text=service_messages.success_choose_dialog_style(name_of_dialog))