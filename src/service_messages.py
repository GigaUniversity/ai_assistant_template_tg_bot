def hello_message(name_of_uni: str):
    text = f'- Привет, я AI-помощник для <b>{name_of_uni}</b>.\n\nЗадай мне свой вопрос!'
    return text


def answer_message(response: dict):
    answer_from_gigachat = response['answer']
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
