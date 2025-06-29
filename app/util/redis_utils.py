import json


async def get_round_state_value(redis_connection, redis_key:str,json_key:str) -> str:
    round_state_bytes = await redis_connection.get(redis_key)
    round_state = json.loads(round_state_bytes)
    current_state = round_state[json_key]
    return current_state