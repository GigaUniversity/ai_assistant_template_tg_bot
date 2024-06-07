from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import os

from source.messages import messages
from source.keyboards import keyboards
from source.config import Config
from source.utils.ai_assistant_api import get_query, post_query
from source.utils.logger_settings import reaction_logger, logger
from source.utils.cache_interactions import form_the_dict_all_responses
from source.utils import files_interactions

user_message_router = Router(name='user_message_router')


@user_message_router.message(CommandStart())
async def hello(message: Message, bot: Bot):
    logger.info(f'Пользователь {message.from_user.id} написал команду /start')
    
    json_path = os.path.join(Config.PROJECT_DIR, "data", "uni_info.json")
    uni_info = files_interactions.json_loads(json_path=json_path)
    list_of_tables = []
    table_status = uni_info.get("table_status")
    for status in table_status:
        if table_status[status] == "True":
            list_of_tables.append(status)
    
    await bot.send_message(chat_id=message.chat.id, text=messages.hello_message(name_of_uni=Config.NAME_OF_UNI),
                           reply_markup=keyboards.choose_the_type_of_content(list_of_tables=list_of_tables))
    

@user_message_router.callback_query(F.data.startswith("choose_the_content_type"))
async def wait_for_your_question(call: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Приём выбранного контент типа
    Сообщение с ожиданием вопроса
    """
    _, content_type = call.data.split('|')
    data = await state.get_data()
    naming_of_table = {"basic": "Обычная информация",
                       "news": "Новости",
                       "timetable": "Расписание",
                       "media": "Медиа"}
    if content_type not in naming_of_table:
        content_type = "basic"
        
    json_path = os.path.join(Config.PROJECT_DIR, "data", "uni_info.json")
    uni_info = files_interactions.json_loads(json_path=json_path)
    table_description = uni_info.get('table_description')
    content_description = table_description[content_type]
    website = uni_info.get("website")

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                text=messages.wait_for_question(uni_name=Config.NAME_OF_UNI,
                                                                content_description=content_description,
                                                                website=website),
                                message_id=call.message.message_id,
                                reply_markup=None)
    await state.update_data(content_type=content_type)

@user_message_router.message()
async def take_query_from_user(message: Message, bot: Bot, state: FSMContext):
    """
    Обрабатываем ответ
    Делаем запрос к API AI-Помощник
    Выдаём ответ от API AI-Помощник
    """
    data = await state.get_data()
    content_type = data.get('content_type', "basic")
    
    logger.info(f'Пользователь {message.from_user.id} задал вопрос: {message.text}')
    text = messages.wait_for_answer()
    msg = await bot.send_message(chat_id=message.chat.id, text=text)
    dialog_style = data.get('dialog_style') if data.get('dialog_style') else 'standart'
    query = {
        'university': Config.UNI_ID,
        'current_question': message.text,
        'dialog_style': dialog_style,
        'chat_id': message.chat.id,
        'datetime_msg': message.date.strftime('%Y-%m-%d %H:%M:%S'),
        'message_id': message.message_id,
        'content_type': content_type
    }
    response = await get_query(params=query, endpoint='/answer')
    current_response = {f'{msg.message_id}': response}
    all_responses = await form_the_dict_all_responses(all_responses=data.get('all_responses'),
                                                        current_response=current_response)
    await state.update_data(all_responses=all_responses)

    text = messages.answer_message(response=response)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                text=text, reply_markup=keyboards.answer_keyboard())
    
    logger.info(
        f'Пользователь {message.from_user.id} на вопрос {message.text} получил ответ {response.get("final_answer")}')
    


@user_message_router.callback_query(F.data == 'button_show_relevant_links')
async def button_show_relevant_links(call: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Обрабатываем кнопку показа релевантных ссылок
    """
    data = await state.get_data()
    all_responses = data.get('all_responses')
    response = all_responses.get(str(call.message.message_id))

    text = messages.show_relevant_links()
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text=text,
                           reply_markup=keyboards.list_of_relevant_links(response))


@user_message_router.callback_query((F.data == 'button_answer_dislike') | (F.data == 'button_answer_like'))
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
    
    text = messages.thanks_for_feedback()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text)
    response_status = await post_query(params=reaction_info, endpoint='/feedback')
    if response_status == 200:
        logger.info(f"Successfully sent feedback to kernel: {reaction_info}")
    else:
        logger.error(f"Failed to send feedback to kernel. Answer: {response_status}. Params: {reaction_info}")

