
from datetime import datetime, timezone
import json

from redis import Redis
from sqlmodel import select
from app.config.db import get_session_sync
from app.config.logger import logger
from app.constants.constant_strings import ConstantStrnigs, RedisKeys, RoundState
from app.models.core_models import CasinoProfitPerRound, Round, Ticket
from app.redis.redis_connection import redis_connection
from app.redis.global_state import set_global_state
from app.util.db_utils import create_db_record, get_db_record


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

    @staticmethod
    async def update_round_and_ticket(round_number:int,multiplier:float):
        try:
            with get_session_sync() as db_session:
                round_to_update=get_db_record(session=db_session,finder=round_number,field="round_number",table=Round)
                if not round_to_update:
                    logger.error(f"Round with number {round_number} not found in database")
                    raise Exception(f"Round with number {round_number} not found in database")
                
                round_to_update.state=RoundState.DONE.value
                round_to_update.multiplier=multiplier
                round_to_update.end_time=datetime.now(timezone.utc)

                logger.info(f"Updating_round_b{round_to_update.round_number} with multiplier {multiplier}")










                # get all the tickets for this round and check if it is a winner populate the payout amount and  other relevant fields
                tickets=db_session.exec(
                    select(Ticket).where(Ticket.round_id == round_to_update.id)
                ).all() 

                for ticket in tickets:
                    if ticket.guessed_multiplier <= multiplier:
                        ticket.is_winner = True
                        ticket.payout_amount = ticket.bet_amount * ticket.guessed_multiplier
                        ticket.actual_multiplier =multiplier
                        logger.info(f"Ticketun {ticket.ticket_code} is a winner with payout amount: {ticket.payout_amount}")
                        
                    else:
                        ticket.is_winner = False
                        ticket.payout_amount = 0.0
                    db_session.add(ticket)


                db_session.commit()
                logger.info(f"Round {round_to_update.round_number} updated_successfully with multiplier {multiplier}")
                db_session.refresh(round_to_update)

                return True
        except Exception as e:
            logger.error(f"Error occured during upating round after round ends{e}")
            raise Exception(f"Error occured during upating round after round ends{e}")
        

    @staticmethod
    async def calculate_casino_profit(round_id: int):
    # get all casinos that place bet in this round

     
        bet_amounts = []
        bet_payouts = []
        profits = []
      
        with get_session_sync() as session:
            stmt = select(Ticket.casino_id).where(Ticket.round_id == round_id).distinct()
            cainos = session.exec(stmt)

            casino_ids = cainos.all()

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
                    
                profit = total_bet_amount - total_payout_amount
                profits.append(profit)
                # logger.info(f"CASINO_PROFIT:{profits}")

                # Here you can calculate commission and other things if needed
                # commission_rate = 0.05  # Example: 5% commission
                # commission_amount = profit * commission_rate

                # # Create or update the CasinoProfitPerRound record 
                #  get the casino_profit record for this round and casino
                
                casino_profit=CasinoProfitPerRound(
                    casino_id=casino_id,
                    round_id=round_id,
                    total_bet_amount=total_bet_amount,
                    total_payout_amount=total_payout_amount,
                    profit=profit,
                    )

                created_casino_profit_db=create_db_record(
                    session=session,
                    table_instance=casino_profit
                )
                if not created_casino_profit_db:
                    logger.error(f"Failed to create casino profit record for casino {casino_id} in round {round_id}")
                    raise Exception(f"Failed to create casino profit record for casino {casino_id} in round {round_id}")
                logger.info(f"Casino profit record created for casino {casino_id} in round {round_id}: {created_casino_profit_db}")
                
               
            
                
                
    
        

    
        
            
        
        