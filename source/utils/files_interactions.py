from ujson import loads
import aiofiles


async def json_loads(json_path) -> dict:
    async with aiofiles.open(json_path, "r", encoding='utf-8') as f:
        return loads(await f.read())


async def parse_string_in_json(json_str: str) -> dict:
    json_dict = loads(json_str)
    return json_dict