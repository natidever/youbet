from fastapi import APIRouter, Depends

from app.api.auth.auth_schemas import AuthSchema, AuthSchemaPost
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
        logger.info(f"casino_ids:{user.casino_id}")
        logger.info(f"to_be_encoded:userid:{user.id},casinoid:{user.casino_id}")
        jwt_encoded=auth_service.create_token(
                data={
                    "role": user.role,
                    "user_id":user.id,
                    "casino_id":user.casino_id
                
                    })
        
        
        logger.info(f"xcasino_id:{user.casino_id,}")

        return AuthSchemaPost(
            username=user.username,
            role=user.role,
            user_id=user.id,
            casino_id=user.casino_id,
            access_token=jwt_encoded,
            is_active=user.is_active
            )
 
