import aiohttp
from source.config import Config
from source.utils.logger_settings import logger


async def get_query(query: dict, endpoint: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{Config.url_to_api}/{endpoint}", params=query) as response:
            return await response.json()


async def post_query(params: dict, endpoint: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{Config.url_to_api}/{endpoint}", params=params) as response:
            return response.status


async def get_answer_from_api(query: dict):
    response = await get_query(query=query, endpoint='answer')
    return response


async def send_feedback_to_api(data: dict):
    status_code = await post_query(params=data, endpoint='feedback')
    if status_code == 200:
        logger.info("Successfully sent feedback to kernel")
    else:
        logger.error("Failed to send feedback to kernel")

