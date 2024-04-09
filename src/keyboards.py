from aiogram.utils.keyboard import InlineKeyboardBuilder


def answer_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Релевантные источники 📖', callback_data='button_show_relevant_links')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def list_of_relevant_links(response: dict):
    keyboard = InlineKeyboardBuilder()
    for i in range(len(response['titles'])):
        keyboard.button(text=response['titles'][i], url=response['urls'][i])
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()
