# В этом модуле лежат все сообщения, требуемые для работы бота


def hello_message(name_of_uni: str):
    text = f'- Привет, я AI-помощник для <b>{name_of_uni}</b>.\n\nЗадай свой вопрос!'
    return text

def answer_message(response: dict):
    answer_from_gigachat = response.get('final_answer')
    service_message = '<i>(Бот работает в тестовом режиме - не все ответы могут быть достоверными)</i>'
    author = '<b>Ответ сгенерирован языковой моделью GigaChat</b>'
    text = answer_from_gigachat + "\n" + service_message + "\n\n" + author
    return text


def wait_for_answer():
    text = 'Ищу ответ..'
    return text


def show_relevant_links():
    text = 'Ниже представлены наиболее релевантные источники для поиска ответа на вопрос.'
    return text


def thanks_for_feedback():
    text = 'Спасибо за оценку! :)'
    return text


def please_take_the_survey(url):
    feedback_url = f'<a href="{url}">ссылке</a>'
    text = f"Будем рады, если Вы пройдете опрос о качестве AI-помощника по данной {feedback_url}."
    return text


def wait_for_question(uni_name: str, content_description: str, website: str):
    content_description = content_description.strip()
    if content_description[-1] != ".":
        content_description += "."
    website = website.strip()
    text = (f"Буду рад найти информацию по {uni_name}.\n\n"
            f"{content_description}\n\n"
            f"Задай мне свой вопрос!\n\n"
            f"<i>Официальный веб-сайт ВУЗа: \n{website}</i>")
    return text


def im_not_working():
    text = 'Я немного устал, но я отвечу сразу, как только отдохну :)'
    return text
