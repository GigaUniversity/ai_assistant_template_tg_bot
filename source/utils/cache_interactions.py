from ujson import loads


async def parse_string_in_json(json_str: str) -> dict:
    json_dict = loads(json_str)
    return json_dict


async def form_the_dict_all_responses(all_responses: dict, current_response: dict):
    """
    Если были запросы,
    то соединение предыдущих запросов с новым, а также удаление из истории старых ответов,
    иначе это единственный запрос в истории
    Длина диалога = 10 сообщениям
    """
    max_history_limit = 10
    if all_responses:
        if isinstance(all_responses, str):
            all_responses = parse_string_in_json(json_str=all_responses)
        if len(all_responses) > max_history_limit - 1:
            min_key = min(all_responses.keys())
            del all_responses[min_key]
        all_responses = {**all_responses, **current_response}
    else:
        all_responses = current_response

    return all_responses