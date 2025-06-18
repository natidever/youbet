
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlmodel import Session
from app.api.auth.auth_service import get_password_hash
from app.api.casino.casino_schemas import CasinoBase, CasinoResponse, UserCreate, UserResponse
from app.config.db import get_session
from app.constants.role import UserRole
from app.models.core_models import Casino, User
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