# AI-Помощник для ВУЗов: Шаблон Telegram-Бота

Шаблон Telegram-Бота с минимальным функционалом.

### Входные данные:
***
* ***URL_TO_API*** - хост для подключения к проекту "AI-Помощник для ВУЗов"
* ***ADMIN_ID*** - Telegram User.id идентификатор Администратора, у которого будут повышенные привелегии (в частности - уведомление о запуске и остановке бота)
* ***TELEGRAM_BOT_TOKEN*** - Telegram Bot API-токен
* ***ACCESS_TOKEN*** - API-токен для подключения к проекту "AI-Помощник для ВУЗов"
* ***UNI_ID*** - идентификатор ВУЗа


### Запуск
***
#### Способ №1: Docker Swarm
> docker swarm init # если Swarm не инициализирован\
> docker stack deploy -c docker-compose-swarm.yml tg_bot

#### Способ №2: Docker Compose
> docker-compose build\
> docker-compose up -d

### Структура проекта
***
* ai_assistant_template_tg_bot/ — корневая директория проекта.
    * .env — файл с переменными окружения
    * data/ — директория для данных.
        * settings.json — файл с настройками проекта .
    * docker-compose-swarm.yml — файл Docker Compose для Swarm режима.
    * Dockerfile — Dockerfile для сборки образа.
    * logs/ — директория для логов.
    * requirements.txt — файл с зависимостями проекта.
    * source/ — директория с исходным кодом.
        * start.py — стартовый файл приложения.
        * config.py — файл конфигурации.
        * handlers/ — директория с обработчиками.
            * __init__.py — файл инициализации пакета.
            * user_commands.py — обработчик пользовательских команд.
            * user_message.py — обработчик пользовательских сообщений.
        * keyboards/ — директория с клавиатурами.
            * keyboards.py — файл с клавиатурами.
        * messages/ — директория с сообщениями.
            * messages.py — файл с сообщениями.
        * utils/ — директория с утилитами.
            * ai_assistant_api.py — HTTP запросы к API проекта.
            * cache_interactions.py — взаимодействие с кэшем.
            * files_interactions.py — взаимодействие с файлами.
            * logger_settings.py — настройки логгера.