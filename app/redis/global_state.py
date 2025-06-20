




import json
from typing import Optional

from redis import Redis

from app.redis.redis_connection import redis_connection
from app.config.logger import logger

def set_global_state(redis:Redis,
                     data:dict,
                     key:str,
                     expire_second:Optional[int]=None
                     ):
    try:
     result= redis.set(name=key,value=json.dumps(data),ex=expire_second)
     if not result:
        logger.error("Unable to set the result")

    except json.JSONEncodeError as e:
        logger.error(f"JSON encoding failed: {str(e)}")

    except Exception as e :
       logger.error("Error occured to save global state of round")

