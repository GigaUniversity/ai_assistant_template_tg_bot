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

# Здесь находятся все обработчики, которые связаны с основной работой бота - первоначальная настройка 
# и обработка вопросов пользователя

router = Router(name='user_message_router')


@router.message(CommandStart())
async def hello(message: Message, bot: Bot):
    """
    /start
    """
    logger.info(f'Пользователь {message.from_user.id} написал команду /start')
    
    json_path = os.path.join(Config.PROJECT_DIR, "data", "uni_info.json")
    uni_info = await files_interactions.json_loads(json_path=json_path)
    name_of_uni = uni_info.get("uni_name")
    
    text = messages.hello_message(name_of_uni=name_of_uni)
    await bot.send_message(chat_id=message.chat.id, 
                           text=text)


@router.message()
async def take_query_from_user(message: Message, state: FSMContext, bot: Bot):
    """
    Обрабатываем ответ
    Делаем запрос к API AI-Помощник
    Выдаём ответ от API AI-Помощник
    """
    logger.info(f'Пользователь {message.from_user.id} задал вопрос: {message.text}')
    
    data = await state.get_data()
    
    text = messages.wait_for_answer()
    msg = await bot.send_message(chat_id=message.chat.id, text=text)
    
    # Формирование параметров запроса к API
    query = {
        'university': Config.UNI_ID,
        'current_question': message.text,
        'chat_id': message.from_user.id,
        'datetime_msg': message.date.strftime('%Y-%m-%d %H:%M:%S'),
        'message_id': message.message_id
    }
    response_status, response_json = await post_query(json=query, endpoint='/answer')
    if response_status == 200:
        text = messages.answer_message(response=response_json)
        reply_markup = keyboards.answer_keyboard(is_ambiguous=response_json['is_ambiguous'])
        msg = await bot.edit_message_text(chat_id=message.chat.id, 
                                          message_id=msg.message_id,
                                          text=text, 
                                          reply_markup=reply_markup)
        
        current_response = {f'{msg.message_id}': response_json}
        all_responses = await form_the_dict_all_responses(all_responses=data.get('all_responses'),
                                                          current_response=current_response)
        await state.update_data(all_responses=all_responses)
        logger_of_success_response = {"user": message.chat.id,
                                      "question": message.text,
                                      "answer": response_json.get('final_answer'),
                                      "rephrase": response_json.get('rephrased_question'),
                                      "titles": response_json.get("titles"),
                                      "urls": response_json.get("urls")
                                      }
        logger.debug(f'Success get query to Kernel "/answer": {logger_of_success_response}')
    else:
        text = messages.im_not_working()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                    text=text)
        logger_of_failed_response = {"user": message.chat.id,
                                     "question": message.text.replace("\n", r"\n"),
                                     "uni": Config.UNI_ID,
                                     "response_status": response_status,
                                     "response_json": response_json}
        logger.warning( f'Failed get query to Kernel "/answer": {logger_of_failed_response}')
    

@router.callback_query(F.data == 'button_show_relevant_links')
async def button_show_relevant_links(call: CallbackQuery, state: FSMContext, bot: Bot):
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


@router.callback_query((F.data == 'button_answer_dislike') | (F.data == 'button_answer_like'))
async def button_answer_reaction(call: CallbackQuery, bot: Bot):
    """
    Обрабатываем кнопку Лайка или Дизлайка
    """
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=keyboards.answer_without_feedback_keyboard())
    reaction = call.data.split('_')[2]
    reaction_info = {'chat_id': call.message.chat.id,
                     'message_id': call.message.message_id,
                     'reaction': reaction}
    reaction_logger.info(reaction_info)
    
    text = messages.thanks_for_feedback()
    await bot.send_message(chat_id=call.message.chat.id, text=text)
    response_status = await post_query(json=reaction_info, endpoint='/feedback')
    if response_status == 200:
        logger.info(f"Successfully sent feedback to kernel: {reaction_info}")
    else:
        logger.error(f"Failed to send feedback to kernel. Answer: {response_status}. Params: {reaction_info}")

