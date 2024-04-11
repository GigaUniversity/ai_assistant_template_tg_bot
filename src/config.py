from dataclasses import dataclass


@dataclass
class Config:
    bot_token = 'YOUR_TOKEN_HERE'
    access_token = 'YOUR_TOKEN_HERE'
    name_of_uni = 'СПбГУ'
    id_of_uni = 'spbu'
    url_to_api = '127.0.0.1:25500'
    admin_id = 0000000
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

