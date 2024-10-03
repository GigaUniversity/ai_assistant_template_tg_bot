# <center>AI-Помощник для ВУЗов: Шаблон Telegram-Бота</center>

Шаблон Telegram-Бота с минимальным функционалом.

### Входные данные
***
* ***URL_TO_API*** - URL для подключения к проекту _"AI-Помощник для ВУЗов"_
* ***ADMIN_ID*** - _Telegram User.id_ идентификатор Администратора, у которого будут повышенные привелегии (в частности - уведомление о запуске и остановке бота)
* ***TELEGRAM_BOT_TOKEN*** - Telegram Bot API-токен
* ***ACCESS_TOKEN*** - API-токен для подключения к проекту _"AI-Помощник для ВУЗов"_
* ***UNI_ID*** - идентификатор вашего ВУЗа


### Запуск
***
#### Способ №1: Docker Compose
```python
docker-compose build
docker-compose up -d
```
#### Способ №2: Manual Python
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m source.start
```

### Структура проекта
***
* ai_assistant_template_tg_bot/ — корневая директория проекта.
    * .env — файл с переменными окружения
    * data/ — директория для данных
        * settings.json — файл с настройками TG бота
    * docker-compose.yml — файл Docker Compose
    * Dockerfile — Dockerfile для сборки образа
    * logs/ — директория для логов
    * requirements.txt — файл с зависимостями проекта
    * source/ — директория с исходным кодом
        * start.py — стартовый файл приложения
        * bot.py — иницализация объектов для работы TG бота
        * lifespan.py — установка цикла жизни TG бота
        * config.py — файл конфигурации
        * handlers/ — директория с обработчиками
            * user_commands.py — обработчик пользовательских команд
            * user_message.py — обработчик пользовательских сообщений
        * keyboards/ — директория с клавиатурами
            * keyboards.py — файл с клавиатурами
        * messages/ — директория с сообщениями
            * messages.py — файл с сообщениями
        * utils/ — директория с утилитами
            * ai_assistant_api.py — HTTP запросы к API проекта
            * cache_interactions.py — взаимодействие с кэшем
            * files_interactions.py — взаимодействие с файлами
            * logger_settings.py — настройки логгера