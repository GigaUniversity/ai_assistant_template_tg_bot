from dataclasses import dataclass
import os
import asyncio

from source.utils.files_interactions import json_loads

@dataclass
class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    NAME_OF_UNI = os.environ.get('NAME_OF_UNI')
    UNI_ID = os.environ.get('UNI_ID')
    URL_TO_API = os.environ.get('URL_TO_API')
    ADMIN_ID = os.environ.get('ADMIN_ID')
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SETTING_PATH = os.path.join(PROJECT_DIR, "data", "settings.json")

