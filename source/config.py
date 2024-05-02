from dataclasses import dataclass
import os


@dataclass
class Config:
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    access_token = os.environ.get('ACCESS_TOKEN')
    name_of_uni = os.environ.get('NAME_OF_UNI')
    id_of_uni = os.environ.get('UNI_ID')
    url_to_api = os.environ.get('URL_TO_API')
    admin_id = os.environ.get('ADMIN_ID')
    styles_of_dialog = [
        {
            "style_name": "Стандартный\uD83D\uDE42",
            "style_id": "standart"
        },
        {
            "style_name": "Педантичный\uD83C\uDF93",
            "style_id": "pedantic"
        },
        {
            "style_name": "Молодёжный\uD83D\uDE0E",
            "style_id": "slang"
        }
    ]

