# this run the game in 4 min interval and send it to redis pub/sub 


import json
from pprint import pprint

from fastapi import Depends
from sqlmodel import Session, select
from app.config.db import get_session, get_session_sync
from app.config.settings import Settings
from app.constants.constant_strings import ConstantStrnigs, RoundState
from app.core.db_utils import create_round
from app.core.game_engine import GameEngine, generate_server_seed
import asyncio
import json
from redis.asyncio import Redis

from app.core.schemas import RoundCreate
from app.models.core_models import Round 
from app.config.logger import logger


settings = Settings()

async def game_runner():
    print(f"url:{settings.REDIS_URL}")
    redis = await Redis.from_url(settings.REDIS_URL)
    pubsub=redis.pubsub()


    print("Game runner started")
    round_number=0
    game = GameEngine()
   

    num_rounds = 1_000_000
    multipliers = []

    while True:

        server_seed_info = generate_server_seed()
        client_seed = game.generate_client_seed()

        round_create=RoundCreate(
            state=RoundState.PENDING.value,
            round_number=round_number,
            server_seed=server_seed_info.seed,
            commitment_hash="test_commitment_hash"
        )

        # creating round before the round starts

        with get_session_sync() as db_session:
             created_round=create_round(round=round_create,session=db_session)
        
        if created_round:
            logger.info(f"created_roud:{created_round}")
        else :
            logger.info(f"round not created:{created_round}")


        # saving the round status 
        
        result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
        logger.info(f"server_seed:{server_seed_info.seed}")
        logger.info(f"clinet_seed:{client_seed}")

        round_number+=1
        multipliers.append(result['multiplier'])
        print(f"Multipler:{result['multiplier']}")


        subscriber_count=await redis.publish(
    ConstantStrnigs.MULTIPLIER_CHANNEL.value,
    json.dumps({
        ConstantStrnigs.MULTIPLIER.value:result['multiplier'],
        ConstantStrnigs.ROUND.value:round_number
    })
)           
        print(f"Published to {subscriber_count} subscribers")


        
        await asyncio.sleep(2)
        yield result['multiplier']
        # publish it to redis 


async def run_game():
    async for multiplier in game_runner():
        pass


if __name__ == "__main__":

    asyncio.run(run_game())




