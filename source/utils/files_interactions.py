import os
import aiofiles
from ujson import loads, dumps

from source.config import Config
from source.utils.ai_assistant_api import get_query


async def json_loads(json_path) -> dict:
    async with aiofiles.open(json_path, "r", encoding='utf-8') as f:
        return loads(await f.read())


async def parse_string_in_json(json_str: str) -> dict:
    json_dict = loads(json_str)
    return json_dict

async def json_save(data: dict, file_path):
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(dumps(data))


async def download_uni_info():
    response_status, json_data = await get_query(endpoint=f"/uni/{Config.UNI_ID}/info/prod", params=None)
    if response_status == 200:
        json_path = os.path.join(Config.PROJECT_DIR, "data", "uni_info.json")
        await json_save(data=json_data, file_path=json_path)
    return response_status, json_data
