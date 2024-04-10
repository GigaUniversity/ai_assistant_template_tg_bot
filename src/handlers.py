from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

import service_messages
import keyboards
from config import Config
from gigachat import get_answer_from_gigachat

router = Router(name='main_router')


@router.message(CommandStart())
async def hello(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.chat.id, text=service_messages.hello_message(name_of_uni=Config.name_of_uni))


@router.message()
async def take_query_from_user(message: Message, bot: Bot, state: FSMContext):
    text = service_messages.wait_for_answer()
    msg = await bot.send_message(chat_id=message.chat.id, text=text)
    query = {
        'university': Config.id_of_uni,
        'current_question': message.text,
        'dialog_style': 'standart',
        'chat_id': message.chat.id,
        # 'message_id': message.message_id,
        # 'datetime': message.date.strftime('%Y-%m-%d %H:%M:%S'),
        # 'gigachat_token': Config.gigachat_token,
    }
    response = await get_answer_from_gigachat(query=query)
    await state.update_data(response=response)

    text = service_messages.answer_message(response=response)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                text=text, reply_markup=keyboards.answer_keyboard())


@router.callback_query(F.data == 'button_show_relevant_links')
async def button_show_relevant_links(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    response = data['response']
    text = service_messages.show_relevant_links()
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboards.list_of_relevant_links(response))