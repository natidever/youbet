from fastapi import APIRouter, Depends

from app.api.casino import casino_service 
from app.api.casino.casino_schemas import CasinoBase, UserCreate
from app.config.db import get_session
from app.constants.role import UserRole
from app.dependencies.auth_dependecies import require_role

casino_router = APIRouter(prefix="/casino",tags=["Casino"])
# casino can be created only by agent or admin
@casino_router.post("/register")
async def register_casino_route(casino:CasinoBase,user:UserCreate,
                                session=Depends(get_session),
                                role=Depends(require_role([UserRole.ADMIN,UserRole.AGENT]))
                                ):

    return casino_service.register_casino_service(session=session,user=user,casino=casino)




