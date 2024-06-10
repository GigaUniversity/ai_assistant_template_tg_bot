from dataclasses import dataclass
import os

@dataclass
class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    UNI_ID = os.environ.get('UNI_ID')
    URL_TO_API = os.environ.get('URL_TO_API')
    ADMIN_ID = os.environ.get('ADMIN_ID')
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SETTING_PATH = os.path.join(PROJECT_DIR, "data", "settings.json")

