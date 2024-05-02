from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from source.messages import service_messages
from source.keyboards import keyboards
from source.config import Config
from source.utils.ai_assistant_api import get_answer_from_api, send_feedback_to_api
from source.utils.logger_settings import reaction_logger, logger
from source.utils.cache_interactions import form_the_dict_all_responses

user_message_router = Router(name='user_message_router')


@user_message_router.message()
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
        'datetime_msg': message.date.strftime('%Y-%m-%d %H:%M:%S'),
        'message_id': message.message_id,
        'access_token': Config.access_token,
    }
    response = await get_answer_from_api(query=query)
    current_response = {f'{msg.message_id}': response}
    data = await state.get_data()
    all_responses = await form_the_dict_all_responses(all_responses=data.get('all_responses'),
                                                      current_response=current_response)
    await state.update_data(all_responses=all_responses)

    text = service_messages.answer_message(response=response)
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

    text = service_messages.show_relevant_links()
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
    text = service_messages.thanks_for_feedback()
    await call.answer(text=text)
    await send_feedback_to_api(data=reaction_info)

