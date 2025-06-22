import json
from fastapi import APIRouter, Depends,HTTPException



from datetime import datetime ,timezone
from app.constants.constant_strings import RedisKeys, RoundState
from app.models.core_models import Round, Ticket
from app.redis.redis_connection import redis_connection
from app.util.db_utils import create_db_record, get_db_record, get_db_record_or_404
from app.util.ticket_utils import geneate_tikcet_code
from app.api.casino import casino_service 
from app.api.casino.casino_schemas import CasinoBase, TicketCreate, TicketResponse, UserCreate
from app.config.db import get_session
from app.config.logger import logger
from app.constants.role import UserRole
from app.dependencies.auth_dependecies import get_current_user, require_role


casino_router = APIRouter(prefix="/casino",tags=["Casino"])
# casino can be created only by agent or admin
@casino_router.post("/register")
async def register_casino_route(
                                casino:CasinoBase,
                                user:UserCreate,
                                session=Depends(get_session),
                                role=Depends(require_role([UserRole.ADMIN,UserRole.AGENT]))
                                ):

    return casino_service.register_casino_service(session=session,user=user,casino=casino)









    
@casino_router.post("/submit-ticket",response_model=TicketResponse)
async def submit_ticket_route(
                              ticket:TicketCreate,
                              session=Depends(get_session),
                              current_user=Depends(get_current_user)
                              ):
    
    return await casino_service.submit_ticket_service(
        ticket=ticket,
        session=session,
        current_user=current_user
    )


@casino_router.post("/resolve-ticket/{ticket_code}")
async def resolve_ticket_route(
    ticket_code: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user)
):
    return await casino_service.resolve_ticket_service(
        ticket_code=ticket_code,
        session=session,
        current_user=current_user
    )



    #  get the ticket code and check if it is for current round and resole it (it is a winner or not)
    


