from fastapi import APIRouter, Depends

from app.api.auth.auth_schemas import AuthSchema
from app.config.db import get_session
from app.api.auth import auth_service
from app.config.logger import logger

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/auth/login")
async def login(auth_data:AuthSchema ,session=Depends(get_session)):
    
    user=auth_service.authenticate_user(session=session,
                      username=auth_data.username,
                      password=auth_data.password
                      )
    logger.debug(f"retrived user when login{user}")
    
    # jwt_encoded=auth_service.create_token(data={user.role})
    

    return user

