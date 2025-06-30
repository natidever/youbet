
from fastapi import logger
from app.constants.constant_strings import RedisKeys, RoundState
from app.redis import redis_connection
from app.redis.global_state import set_global_state


class AfterRoundResolution:
    @staticmethod
    async def update_global_state_after_round(round_number:int):
        after_game_round_data={"round_number":round_number,"round_state":RoundState.DONE.value}
        await set_global_state(
            
                redis=redis_connection,
                key=RedisKeys.CURRENT_ROUND.value,
                data=after_game_round_data
            )
        logger.info(f"Updated_global state for after round: {round_number}  DONE")
        