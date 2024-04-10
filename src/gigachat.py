import aiohttp
from config import Config


async def connect_to_gigachat(query: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=Config.url_to_api, params=query) as response:
            return await response.json()


async def get_answer_from_gigachat(query: dict):
    response = await connect_to_gigachat(query=query)
    return response

