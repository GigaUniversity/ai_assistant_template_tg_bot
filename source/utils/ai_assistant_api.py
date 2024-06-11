import aiohttp
from aiohttp.client_exceptions import ContentTypeError

from source.utils.logger_settings import logger
from source.config import Config

headers = {'Authorization': 'Bearer ' + Config.ACCESS_TOKEN}

async def get_query(params: dict, endpoint: str):
    url = f"{Config.URL_TO_API}{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.get(headers=headers, url=url, params=params) as response:
            try:
                return response.status, await response.json()
            except Exception as e:
                log_error_dict = {"where": "get_query",
                                  "url": url,
                                  "error": e,
                                  "response_status": response.status,
                                  "response_text": await response.text}
                logger.error(log_error_dict)
                return response.status, None


async def post_query(params: dict, endpoint: str):
    url = f"{Config.URL_TO_API}{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.post(headers=headers, url=url, params=params) as response:
            try:
                return response.status
            except ContentTypeError as e:
                log_error_dict = {"where": "post_query",
                                  "url": url,
                                  "error": e,
                                  "response_status": response.status,
                                  "response_text": await response.text}
                logger.error(log_error_dict)
                return response.status
