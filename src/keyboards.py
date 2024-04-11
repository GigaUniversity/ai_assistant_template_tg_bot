from aiogram.utils.keyboard import InlineKeyboardBuilder


def answer_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Релевантные источники 📖', callback_data='button_show_relevant_links')
    keyboard.button(text='👎', callback_data='button_answer_dislike')
    keyboard.button(text='👍', callback_data='button_answer_like')
    keyboard.adjust(1, 2)
    return keyboard.as_markup()


def answer_without_feedback_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Релевантные источники 📖', callback_data='button_show_relevant_links')
    return keyboard.as_markup()


def list_of_relevant_links(response: dict):
    keyboard = InlineKeyboardBuilder()
    for i in range(len(response['titles'])):
        keyboard.button(text=response['titles'][i], url=response['urls'][i])
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def choose_the_style(styles_list: list):
    keyboard = InlineKeyboardBuilder()
    for style in styles_list:
        keyboard.button(text=style['style_name'], callback_data=f"choose_the_style|{style['style_id']}")
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()