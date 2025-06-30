
import asyncio
from time import time
from app.config.db import get_session_sync
from app.constants.constant_strings import RedisKeys, RedisRoundNumberGeneratorCircuitState, RoundState
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

      return  await RoundNumberGenerator.get_round_number()
        # try:
        #  round_number = await redis_connection.incr(RedisKeys.CURRENT_ROUND_NUMBER.value)
        #  logger.info(f"Round number from redis: {round_number}")
        #  return round_number
        # except Exception as e:
        #     logger.error(f"Error getting round number from redis: {e}")
        #     raise Exception(f"Error getting round number from redis: {e}")
    







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
        








class RoundNumberGenerator:
    

    _circuit_state=RedisRoundNumberGeneratorCircuitState.CLOSED
    _last_failure_time = 0
    _last_round_number = None
    _failure_count = 0
    _lock = asyncio.Lock() 


    



    REST_TIME_OUT= 60 
    MAX_FAILURES = 3  # After 3 failures, trip the circuit

    
    @staticmethod
    async def get_round_number():
        if RoundNumberGenerator._circuit_state == RedisRoundNumberGeneratorCircuitState.OPEN and time.time() < RoundNumberGenerator._last_failure_time + RoundNumberGenerator.REST_TIME_OUT:
            logger.warning("Circuit is open, cannot generate round number at this time.")
            raise Exception("Circuit is open, cannot generate round number at this time.")
        elif RoundNumberGenerator._circuit_state == RedisRoundNumberGeneratorCircuitState.OPEN:
             RoundNumberGenerator._circuit_state = RedisRoundNumberGeneratorCircuitState.HALF_OPEN
        
        async with RoundNumberGenerator._lock:
            try:
                return await RoundNumberGenerator._generate_round_number()
           
            except Exception as e:
                raise Exception(f"Error generating round number: {e}")






    @classmethod
    async def _generate_round_number(cls):
        round_number = await redis_connection.incr(RedisKeys.CURRENT_ROUND_NUMBER.value)

        if cls._last_round_number and round_number <=cls._last_round_number:
            cls._failure_count += 1
            logger.warning(f"Duplicate detected! Redis:{round_number} Last:{cls._last_round_number}")
       

            # here the recover begin
    
            if cls._failure_count >= cls.MAX_FAILURES:
                cls._circuit_state = RedisRoundNumberGeneratorCircuitState.OPEN
                cls._last_failure_time = time.time()
                logger.error(f"Circuit tripped after {cls._failure_count} failures. Circuit state: {cls._circuit_state}")
                raise Exception("Circuit is open, cannot generate round number at this time.")
            round_number = cls._last_round_number + 1
            await redis_connection.set(RedisKeys.CURRENT_ROUND_NUMBER.value, round_number)
            logger.info(f"Round number reset to {round_number} due to duplicate detection.")


        if cls._circuit_state == RedisRoundNumberGeneratorCircuitState.HALF_OPEN:
            cls._circuit_state = RedisRoundNumberGeneratorCircuitState.CLOSED
            cls._failure_count = 0
            logger.info("Circuit closed after successful round number generation.")
        cls._last_round_number = round_number
        logger.info(f"Generated round number: {round_number}")
        return round_number

            

           
       
       
    

    

  