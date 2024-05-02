from dataclasses import dataclass
import os
import asyncio

from source.utils.files_interactions import json_loads


async def get_settings(project_dir) -> dict:
    return await json_loads(os.path.join(project_dir, "source", "data", "settings.json"))

@dataclass
class Config:
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    access_token = os.environ.get('ACCESS_TOKEN')
    name_of_uni = os.environ.get('NAME_OF_UNI')
    id_of_uni = os.environ.get('UNI_ID')
    url_to_api = os.environ.get('URL_TO_API')
    admin_id = os.environ.get('ADMIN_ID')
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    styles_of_dialog = asyncio.run(get_settings(project_dir=project_dir))['styles_of_dialog']
    commands_for_bot = asyncio.run(get_settings(project_dir=project_dir))['commands_for_bot']

