def hello_message(name_of_uni: str):
    text = f'- Привет, я AI-помощник для <b>{name_of_uni}</b>.\n\nЗадай мне свой вопрос!'
    return text


def answer_message(response: dict):
    print(response)
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

def choose_your_style():
    text = f"Выберите стиль диалога!"
    return text


def success_choose_dialog_style(name_of_style):
    text = (f"{name_of_style} стиль диалога успешно выбран!\n"
            f"Теперь вы можете задать свой вопрос и я отвечу в выбранном стиле 😊")
    return text