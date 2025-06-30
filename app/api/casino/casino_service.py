
from datetime import datetime
import json
from typing import Dict
from app.constants.constant_strings import RedisKeys, RoundState
from app.redis.redis_connection import redis_connection
from app.util.db_utils import create_db_record, get_db_record, get_db_record_or_404
from app.util.redis_utils import get_round_state_value
from app.util.ticket_utils import geneate_tikcet_code
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlmodel import Session
from app.api.auth.auth_service import get_password_hash
from app.api.casino.casino_schemas import CasinoBase, CasinoResponse, TicketCreate, TicketResolveResponse, TicketResponse, UserCreate, UserResponse
from app.config.db import get_session
from app.constants.role import UserRole
from app.models.core_models import Casino, Round, Ticket, User
from app.config.logger import logger

def register_casino_service(casino:CasinoBase,user:UserCreate,session:Session)->CasinoResponse:
   try:
        
     #    creating casino 
        casino =Casino(
            name=casino.name,
            contact_email=casino.contact_email,
            contact_phones=casino.contact_phones
        )
        existing_casino=session.exec(
             select(Casino).where(Casino.contact_email ==casino.contact_email)
        ).first()

        if existing_casino:
             raise HTTPException(status_code=400, detail="casino with this email already exists")

        session.add(casino)
        session.flush()

        hashed_user_password=get_password_hash(user.password)
      
     #    creating user connected to user to add their 

     #    
      
        logger.info(f"casino_idxz:{casino.id}")

        casino_user = User(
        username=user.username,
        password_hash=hashed_user_password,
        role=UserRole.CASINO,
        casino_id=casino.id

    )    
     
       
        existing_user= session.exec(select(User).where(User.username ==user.username)).first()
        if existing_user:
                raise HTTPException(status_code=400, detail="Username already exists")



        session.add(casino_user)
        session.commit()
        session.refresh(casino)
        session.refresh(casino_user)


        return CasinoResponse(
        name=casino.name,
        contact_email=casino.contact_email,
        contact_phones=casino.contact_phones,
    
       user_id=casino_user.id,
       casino_id=casino.id,
       is_active=casino_user.is_active,  
       role=casino_user.role.value, 
   
       user=UserResponse(
        username=casino_user.username
    )
)

        

        
     
   except Exception as e :
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating casino+user: {str(e)}"
        )
   





async def submit_ticket_service(
        session:Session,
        current_user:Dict[str,any],
        ticket:TicketCreate

):
   current_round_number= await redis_connection.get(RedisKeys.CURRENT_ROUND_NUMBER.value)
    #2. fetch the current round_id using the redis key

   current_db_round=get_db_record_or_404(
                    session=session,
                    finder=int(current_round_number),
                    table=Round,
                    field="round_number",
                    error_message="round not found")
    
    # 3.get the casino_id from the current user
   casino_id=current_user["casino_id"]
    #4. Getting redis-data
   round_state_bytes=await redis_connection.get(RedisKeys.CURRENT_ROUND.value)


   round_state = json.loads(round_state_bytes.decode('utf-8'))
   current_state = round_state["round_state"]

   logger.info(f"rond_state_cc:{current_state}")
    # 5.creating ticket
   if current_state == RoundState.PENDING.value:
        # 5.1 generating ticket code 
       ticket_code=geneate_tikcet_code(casino_id=casino_id,
                                       round_number=current_round_number,
                                       guessed_multiplier=ticket.guessed_multiplier,
                                       timestamp=int(datetime.now().timestamp())
                                       
                                       )
       logger.info(f"geneated_ticket_code: {ticket_code}")
        # 5.2 preparing ticket instance for creatoin
       ticket_instance=Ticket(
           casino_id=casino_id,
           round_id=current_db_round.id,
           ticket_code=ticket_code,
           guessed_multiplier=ticket.guessed_multiplier,
    
           bet_amount=ticket.bet_amount
           
           
       )


       existing_ticket= get_db_record(
           session=session,field="ticket_code",finder=ticket_code,table=Ticket
       )
       print(f"exisst{existing_ticket}")
       if  existing_ticket:
         raise HTTPException(status_code=400,detail="ticket already existed")

        # creating ticket on db
       created_ticket= create_db_record(session=session,table_instance=ticket_instance)
       return TicketResponse(
           id=created_ticket.id,
           payout_amount=created_ticket.bet_amount*created_ticket.guessed_multiplier,
           round_id=current_db_round.id,
           ticket_code=created_ticket.ticket_code,
           guessed_multiplier=created_ticket.guessed_multiplier,
           bet_amount=created_ticket.bet_amount,
           round_number=int(current_round_number),

           
           
       )
    #    return {"ticksetxxxx":created_ticket,"cs":current_db_round,"stssate":round_state}


       
   elif current_state == RoundState.DONE.value:
       raise HTTPException(status_code=400,detail="Round is done")
   else:
       raise HTTPException(status_code=500,detail="Unexpected error")
   


async def resolve_ticket_service(
        session:Session,
        ticket_code:str,
        current_user:Dict[str, any]
):
  current_round_state= await get_round_state_value(redis_connection=redis_connection, redis_key=RedisKeys.CURRENT_ROUND.value, json_key="round_state")

  logger.info(f"stateue:{current_round_state}")
    # 1. get the current user casino

  
    # 1. get the ticket from db
  ticket=get_db_record_or_404(
        session=session,
        finder=ticket_code,
        table=Ticket,
        field="ticket_code",
        error_message="ticket not found"
    )
    # 2. get the current round from redis and  check if the ticket is from that round
  current_round_number_byte = await redis_connection.get(RedisKeys.CURRENT_ROUND_NUMBER.value)
#   change byte redis to int
  current_round= int(current_round_number_byte.decode('utf-8'))
  
  
  logger.info(f"current_round_numbexr:{current_round}")
    #3.get the ticket round from db 
  ticket_round=get_db_record_or_404(
            session=session,
            finder=ticket.round_id,
            table=Round,
            field="id",
            error_message="round not found"
        )
  
#   return validate_ticket(ticket_round=ticket_round,ticket=ticket,current_round=current_round)
  return {"state":current_round_state}
    # 4. check if the ticket is from the previos round
    
#   validate_ticket()
#   if ticket_round.round_number != int(current_round-1):
#         raise HTTPException(status_code=400, detail="Ticket is not from the previous round")
#   if ticket_round.is_redeemed:
#         raise HTTPException(status_code=400, detail="Ticket has already been redeemed")
  
#   if ticket.guessed_multiplier >=ticket_round.multiplier: 
#       ticket.is_winner = True
#       ticket.payout_amount = ticket.bet_amount * ticket.guessed_multiplier 
      
  


#   return {"is_winner":True,"payout_amount":ticket.payout_amount,"multiplier":ticket_round.multiplier}

    # 5. Check if the ticket is already redeemed 
    #6 check if the ticket is winning ticket if so return the payout amount

  
       

   

     
def validate_ticket(ticket_round:Round,ticket:Ticket,current_round:str)->TicketResolveResponse:
  if ticket_round.round_number != int(current_round-1):
        return HTTPException(status_code=400, detail="Ticket is not from the previous round")
  if ticket.is_redeemed:
        return HTTPException(status_code=400, detail="Ticket has already been redeemed")
  
  if ticket.guessed_multiplier <=ticket_round.multiplier: 
      ticket.is_winner = True
      ticket.payout_amount = ticket.bet_amount * ticket.guessed_multiplier 
    #   ticket.is_redeemed = True
    #   here tax and other things can be applied
      return TicketResolveResponse(
          ticket_code=ticket.ticket_code,
          is_winner=ticket.is_winner,
          actual_multiplier=ticket_round.multiplier,
          payout_amount=ticket.payout_amount,
          round_id=ticket_round.id,
          round_number=ticket_round.round_number
      )
  else:
        ticket.is_winner = False
        ticket.payout_amount = 0.0
        return TicketResolveResponse(
            ticket_code=ticket.ticket_code,
            is_winner=ticket.is_winner,
            actual_multiplier=ticket_round.multiplier,
            payout_amount=ticket.payout_amount,
            round_id=ticket_round.id,
            round_number=ticket_round.round_number
        )

    
     

    #  this will be changed to just quring the database since already populated after the game ends
    # we might only set is reedemd to true rather than calucalting the payout and other filed because 
    # we already have the is winner and the payout populated after the round ends 