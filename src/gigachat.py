import requests
from config import Config as config



async def connect_to_gigachat(query: dict):
    response = requests.post(url=config.url_to_api, json=query)
