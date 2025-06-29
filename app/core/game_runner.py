# this run the game in 4 min interval and send it to redis pub/sub 


from datetime import datetime, timezone
import json
from pprint import pprint
from app.util.db_utils import get_db_record
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
from app.models.core_models import Round, Ticket 
from app.config.logger import logger
from app.redis.redis_connection import redis_connection
from app.redis.global_state import set_global_state
from app.util.redis_utils import get_round_state_value


settings = Settings()



def calculate_casino_profit(
    session: Session,
    round_id: int
):
    # get all casinos that place bet in this round

    stmt = select(Ticket.casino_id).where(Ticket.round_id == round_id).distinct()
    cainos = session.exec(stmt)

    casino_ids = cainos.all()

    logger.info(f"cal_Called:")
    bet_amounts = []
    bet_payouts = []

    #calculate the profit for each casino 
    for casino_id in casino_ids:
        # casino_id = casino_id  # Extract the actual ID from the tuple
        logger.info(f"CASINO_ID:{casino_id}")
        # get all tickets for this casino
        tickets = session.exec(
            select(Ticket).where(Ticket.casino_id == casino_id, Ticket.round_id == round_id)
        ).all()

        total_bet_amount = sum(ticket.bet_amount for ticket in tickets)
        total_payout_amount = sum(ticket.payout_amount for ticket in tickets if ticket.is_winner)
        bet_amounts.append(total_bet_amount)
        bet_payouts.append(total_payout_amount)
    logger.info(f"total_bet:{bet_amounts}")
    logger.info(f"xpayout:{bet_payouts}")
        # profit = total_bet_amount - total_payout_amount

        # Here you can calculate commission and other things if needed
        # commission_rate = 0.05  # Example: 5% commission
        # commission_amount = profit * commission_rate

        # # Create or update the CasinoProfitPerRound record
        # casino_profit = get_db_record(
        #     session=session,
        #     finder=round_id,
        #     table=Round,
        #     field="id"
        # )

        # if not casino_profit:
        #     raise Exception("Casino profit record not found")

        # casino_profit.total_bet_amount = total_bet_amount
        # casino_profit.total_payout_amount = total_payout_amount
        # casino_profit.profit = profit
        # casino_profit.commission_rate = commission_rate
        # casino_profit.commission_amount = commission_amount
     





















async def game_runner():
    # print(f"url:{settings.REDIS_URL}")
    redis = await Redis.from_url(settings.REDIS_URL)
    pubsub=redis.pubsub()


    # print("Game runner started")
    # round_number=0
    game = GameEngine()
   


    multipliers = []

    while True:
        logger.info("NEW_ROUND_STARTING")

        server_seed_info = generate_server_seed()
        client_seed = game.generate_client_seed()

        
        round_number=await redis_connection.incr(RedisKeys.CURRENT_ROUND_NUMBER.value)
        
        # logger.info(F"ROUND_NUMBER_FROM_REDIS {round_number[0]}")
        logger.info(                

                f"ROUND_FROM_RUNNER{round_number}_PENDING "



        )
     

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
           logger.info(f"Creating round with number: {round_create.round_number}")
           created_round= create_round(round=round_create,session=db_session)
           logger.info(f"created_roundx:{created_round.id}")

        except Exception as e:
            logger.error(f"Error creating round: {e}")
            created_round=None
            raise Exception(f"Error creating round: {e}")




















        # here people can register
        
        

        before_game_round_data={"round_number":round_number,"round_state":RoundState.PENDING.value}
        if created_round:
            # logger.info(f"created_roud:{created_round}")
           try:
            await set_global_state(
                    redis=redis_connection,
                    key=RedisKeys.CURRENT_ROUND.value,
                    data=before_game_round_data
                )   
           except Exception as e:
                logger.error(f"Error setting global state: {e}")
                raise Exception(f"Error setting global state: {e}")
           
        else :
            logger.info(f"round not created:{created_round}")


        # 4minute gap
        await asyncio.sleep(30)

        
        result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
        # logger.info(f"server_seed:{server_seed_info.seed}")
        # logger.info(f"clinet_seed:{client_seed}")




        multipliers.append(result['multiplier'])
        
        print(f"Multipler:{result['multiplier']}")
        logger.info(f"server_seed:{server_seed_info.seed}")

        
        """ HERE UPDATE THE GLOBAL STATE OF REDIS AND DATABASE FOR CURRENT ROUND
            UPDATE THE DB ALSO HERE 
         
           DATA"""
         
        #  round state multiplier and othr thing:

        

            


         

        after_game_round_data={"round_number":round_number,"round_state":RoundState.DONE.value}
        await set_global_state(
            
                redis=redis_connection,
                key=RedisKeys.CURRENT_ROUND.value,
                data=after_game_round_data
            )
        
        
        logger.info(                

                f"ROUNDR_{round_number}_DONE_MULTIPLIER_{result['multiplier']}"  



        )
        current_round_state= await get_round_state_value(redis_connection=redis_connection, redis_key=RedisKeys.CURRENT_ROUND.value, json_key="round_state")


        logger.info(                

                f"AFTERROUND_{current_round_state}"



        )
        

        #
      

        subscriber_count=await redis.publish(
    ConstantStrnigs.MULTIPLIER_CHANNEL.value,
    json.dumps({
        ConstantStrnigs.MULTIPLIER.value:result['multiplier'],
        ConstantStrnigs.ROUND.value:round_number
    })
)      
        print(f"Published to {subscriber_count} subscribers")

        try:
            with get_session_sync() as db_session:
                round_to_update=get_db_record(session=db_session,finder=round_number,field="round_number",table=Round)
                if not round_to_update:
                    logger.error(f"Round with number {round_number} not found in database")
                    continue
                round_to_update.state=RoundState.DONE.value
                round_to_update.multiplier=result['multiplier']
                round_to_update.end_time=datetime.now(timezone.utc)

                casinos=calculate_casino_profit(
                    session=db_session,
                    round_id=round_to_update.id)
                
                logger.info(f"CASINOSwe:{casinos}")






                db_session.commit()
                db_session.refresh(round_to_update)
                print(f"updated:{pprint(vars(round_to_update))}")
                print(f"updatedx:{round_to_update}")
        except Exception as e:
            logger.error("Error occured during upating round after round ends")
            raise


        
        # await asyncio.sleep(30)
        yield result['multiplier']
        # publish it to redis 
    

async def run_game():
    async for multiplier in game_runner():
        pass


if __name__ == "__main__":

    asyncio.run(run_game())





























