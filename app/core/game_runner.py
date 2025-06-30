# this run the game in 4 min interval and send it to redis pub/sub 


from datetime import datetime, timezone
import json
from pprint import pprint
from app.core.after_round_resolution import AfterRoundResolution
from app.core.before_round_preparation import BeforeRoundPreparation
from app.util.db_utils import create_db_record, get_db_record
from fastapi import Depends
from sqlmodel import Session, select
from app.config.db import get_session, get_session_sync
from app.config.settings import Settings
from app.constants.constant_strings import ConstantStrnigs, RedisKeys, RoundState
from app.core.helpers import create_round
from app.core.game_engine import GameEngine, generate_server_seed
import asyncio
import json
from redis.asyncio import Redis

from app.core.schemas import RoundCreate
from app.models.core_models import CasinoProfitPerRound, Round, Ticket 
from app.config.logger import logger
from app.redis.redis_connection import redis_connection
from app.redis.global_state import set_global_state
from app.util.redis_utils import get_round_state_value


settings = Settings()





async def game_runner():
    # print(f"url:{settings.REDIS_URL}")
    redis = await Redis.from_url(settings.REDIS_URL)
    pubsub=redis.pubsub()


    # print("Game runner started")
    # round_number=0
    game = GameEngine()
   


    multipliers = []

    while True:
       # before round start here 
        
        server_seed_info,client_seed= await BeforeRoundPreparation.generate_seeds(game=game)
        round_number=await BeforeRoundPreparation.get_round_number()
       


        created_round=await BeforeRoundPreparation.create_round(round_number=round_number, server_seed_info=server_seed_info)



        if created_round:

            await BeforeRoundPreparation.set_gloabl_state_before_round(round_number=round_number)
 
        else:
            logger.info(f"round not created:{created_round}")


        # Wait for registration before the multiplier is generated
        await asyncio.sleep(15)

        
        result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
        multipliers.append(result['multiplier'])
        print(f"Multiplerx:{result['multiplier']}")
        logger.info(f"server_seed:{server_seed_info.seed}")

    
        await AfterRoundResolution.update_global_state_after_round(round_number=round_number)
        current_round_state= await get_round_state_value(redis_connection=redis_connection, redis_key=RedisKeys.CURRENT_ROUND.value, json_key="round_state")

        logger.info( f"AFTERROUND_xyz{current_round_state}")
    
       
        await AfterRoundResolution.publish_to_websocket(redis=redis,multipler=result['multiplier'], round_number=round_number)
        

        db_update_result = await AfterRoundResolution.update_round_and_ticket(
            round_number=round_number,
            multiplier=result['multiplier']
        )

        if db_update_result:
            await AfterRoundResolution.calculate_casino_profit(round_id=created_round.id)
            
        yield result['multiplier']
        
    

async def run_game():
    async for multiplier in game_runner():
        pass


if __name__ == "__main__":

    asyncio.run(run_game())





























