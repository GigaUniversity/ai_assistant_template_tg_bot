from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class Config:
    """
    TELEGRAM_BOT_TOKEN - API ключ Телеграм Бота
    ACCESS_TOKEN - API ключ для подключения к проекту AI-Помощник для ВУЗов
    UNI_ID - идентификатор университета
    URL_TO_API - хост для взаимодействия с проектом AI-Помощник для ВУЗов
    ADMIN_ID - Telegram user_id пользователя с повышенным доступом
    PROJECT_DIR - путь к директории с проектом
    SETTING_PATH - путь к настройкам
    """
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    UNI_ID = os.environ.get('UNI_ID')
    URL_TO_API = os.environ.get('URL_TO_API')
    ADMIN_ID = os.environ.get('ADMIN_ID')
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SETTING_PATH = os.path.join(PROJECT_DIR, "data", "settings.json")

