
from app.config.db import get_session_sync
from app.constants.constant_strings import RedisKeys, RoundState
from app.core.game_engine import generate_server_seed
from app.core.helpers import create_round
from app.core.schemas import RoundCreate
from app.redis.redis_connection import redis_connection
from app.config.logger import logger
from app.redis.global_state import set_global_state

class BeforeRoundPreparation:
    """
    This class is responsible for preparing the game before a new round starts.
    It do the following 
    1.Generate server seed and client seed.
    2.Create a new round in the database.
    3.Set the global state for the current round.
    """

    @staticmethod
    async def generate_seeds(game):
        try:
            server_seed_info = generate_server_seed()
            client_seed = game.generate_client_seed()
            logger.info(f"seeds_generated: server_seed={server_seed_info.seed}, client_seed={client_seed}")
            return server_seed_info, client_seed,
        except Exception as e:
            logger.error(f"Error generating seeds: {e}")
            raise Exception(f"Error generating seeds: {e}")



    @staticmethod
    async def get_round_number():
        try:
         round_number = await redis_connection.incr(RedisKeys.CURRENT_ROUND_NUMBER.value)
         logger.info(f"Round number from redis: {round_number}")
         return round_number
        except Exception as e:
            logger.error(f"Error getting round number from redis: {e}")
            raise Exception(f"Error getting round number from redis: {e}")
    







    @staticmethod
    async def create_round(round_number, server_seed_info):
        round_create=RoundCreate(
            state=RoundState.PENDING.value,
            # 
            round_number=round_number,
            
            server_seed=server_seed_info.seed,
            commitment_hash="test_commitment_hash"
        )

        # creating round before the round starts

        try:
         with get_session_sync() as db_session:
           logger.info(f"Creating_round with number: {round_create.round_number}")
           created_round= create_round(round=round_create,session=db_session)
           logger.info(f"created_roundx:{created_round.id}")
          

        except Exception as e:
            logger.error(f"Error creating round: {e}")
            created_round=None
            raise Exception(f"Error creating round: {e}")
        
        return created_round
    
    @staticmethod
    async def set_gloabl_state_before_round(round_number:int):
        logger.info(f"Setting_global state for round number: {round_number}")
       
        before_game_round_data={"round_number":round_number,"round_state":RoundState.PENDING.value}

        try:
            await set_global_state(
                    redis=redis_connection,
                    key=RedisKeys.CURRENT_ROUND.value,
                    data=before_game_round_data
                )   
        except Exception as e:
                logger.error(f"Error setting global state: {e}")
                raise Exception(f"Error setting global state: {e}")
           
       
       
    

    

  