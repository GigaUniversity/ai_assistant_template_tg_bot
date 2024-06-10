import aiohttp
from source.config import Config

headers = {'Authorization': 'Bearer ' + Config.ACCESS_TOKEN}

async def get_query(params: dict, endpoint: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{Config.URL_TO_API}{endpoint}", params=params) as response:
            return response.status, await response.json()


async def post_query(params: dict, endpoint: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{Config.URL_TO_API}{endpoint}", params=params) as response:
            return response.status
