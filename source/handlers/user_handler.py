from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from source.messages import service_messages
from source.keyboards import keyboards
from source.config import Config
from source.utils.ai_assistant_api import get_answer_from_api, send_feedback_to_api
from source.utils.logger_settings import reaction_logger, logger

router = Router(name='main_router')


@router.message(CommandStart())
async def hello(message: Message, bot: Bot):
    logger.info(f'Пользователь {message.from_user.id} написал команду /start')
    await bot.send_message(chat_id=message.chat.id, text=service_messages.hello_message(name_of_uni=Config.name_of_uni))


@router.message()
async def take_query_from_user(message: Message, bot: Bot, state: FSMContext):
    """
    Обрабатываем ответ
    Делаем запрос к API AI-Помощник
    Выдаём ответ от API AI-Помощник
    """
    logger.info(f'Пользователь {message.from_user.id} задал вопрос: {message.text}')
    text = service_messages.wait_for_answer()
    msg = await bot.send_message(chat_id=message.chat.id, text=text)
    data = await state.get_data()
    dialog_style = data.get('dialog_style') if data.get('dialog_style') else 'standart'
    query = {
        'university': Config.id_of_uni,
        'current_question': message.text,
        'dialog_style': dialog_style,
        'chat_id': message.chat.id,
        'source': 'telegram',
        'datetime': message.date.strftime('%Y-%m-%d %H:%M:%S'),
        'message_id': message.message_id,
        'access_token': Config.access_token,
    }
    response = await get_answer_from_api(query=query)
    await state.update_data(response=response)

    text = service_messages.answer_message(response=response)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                text=text, reply_markup=keyboards.answer_keyboard())
    logger.info(f'Пользователь {message.from_user.id} на вопрос {message.text} получил ответ {response["final_answer"]}')


@router.callback_query(F.data == 'button_show_relevant_links')
async def button_show_relevant_links(call: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Обрабатываем кнопку показа релевантных ссылок
    """
    data = await state.get_data()
    response = data['response']
    text = service_messages.show_relevant_links()
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboards.list_of_relevant_links(response))


@router.callback_query(F.data == 'button_answer_dislike' or F.data == 'button_answer_like')
async def button_answer_reaction(call: CallbackQuery, bot: Bot):
    """
    Обрабатываем кнопку Лайка или Дизлайка
    """
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=keyboards.answer_without_feedback_keyboard())
    reaction = call.data.split('_')[2]
    reaction_info = {'chat_id': call.message.chat.id,
                     'username': call.message.from_user.username,
                     'message_id': call.message.message_id,
                     'reaction': reaction}
    reaction_logger.info(reaction_info)
    text = service_messages.thanks_for_feedback()
    await call.answer(text=text)
    await send_feedback_to_api(data=reaction_info)


@router.message(Command('styles'))
async def command_styles(message: Message, bot: Bot):
    """
    Обработчик команды по поводу смены стиля диалога
    """
    await bot.send_message(chat_id=message.chat.id, text=service_messages.choose_your_style(),
                           reply_markup=keyboards.choose_the_style(styles_list=Config.styles_of_dialog))


@router.callback_query(F.data.startswith("choose_the_style"))
async def choose_the_uni(bot: Bot, call: CallbackQuery, state: FSMContext):
    """
    Выбор конкретного стиля диалога
    """
    _, dialog_style = call.data.split('|')
    name_of_dialog = call.message.reply_markup.inline_keyboard[0][0].text
    await state.update_data(dialog_style=dialog_style)
    await bot.send_message(chat_id=call.message.chat.id,
                           text=service_messages.success_choose_dialog_style(name_of_dialog))