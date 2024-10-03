from aiogram.utils.keyboard import InlineKeyboardBuilder


# В этом модуле лежат все Inline-клавиатуры

def answer_keyboard(is_ambiguous: bool):
    keyboard = InlineKeyboardBuilder()
    if not is_ambiguous:
        keyboard.button(text='📖 Релевантные источники', callback_data='button_show_relevant_links')
    keyboard.button(text='👎', callback_data='button_answer_dislike')
    keyboard.button(text='👍', callback_data='button_answer_like')
    keyboard.adjust(1, 2)
    return keyboard.as_markup()


def answer_without_feedback_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='📖 Релевантные источники', callback_data='button_show_relevant_links')
    return keyboard.as_markup()


def list_of_relevant_links(response: dict):
    """
    Показ релевантных ссылок
    """
    keyboard = InlineKeyboardBuilder()
    added_urls = set()

    combined_list = [{"title": title, "url": url} for title, url in zip(response["titles"], response["urls"])]
    for item in combined_list:
        if item["url"].strip() not in added_urls:
            keyboard.button(text=item['title'], url=item['url'])
            added_urls.add(item["url"].strip())
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()