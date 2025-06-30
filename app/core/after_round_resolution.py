
import json

from redis import Redis
from app.config.logger import logger
from app.constants.constant_strings import ConstantStrnigs, RedisKeys, RoundState
from app.redis.redis_connection import redis_connection
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


    @staticmethod
    async def publish_to_websocket(redis:Redis, multipler:float, round_number:int,):

        subscriber_count=await redis.publish(
        ConstantStrnigs.MULTIPLIER_CHANNEL.value,
        json.dumps({
            ConstantStrnigs.MULTIPLIER.value:multipler,
            ConstantStrnigs.ROUND.value:round_number
        })
    )      
        logger.info(f"Published to {subscriber_count} subscribers")
            
        
        