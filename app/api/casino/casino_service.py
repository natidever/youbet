
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlmodel import Session
from app.api.auth.auth_service import get_password_hash
from app.api.casino.casino_schemas import CasinoBase, UserCreate
from app.config.db import get_session
from app.constants.role import UserRole
from app.models.core_models import Casino, User

def register_casino_service(casino:CasinoBase,user:UserCreate,session:Session):
   try:
        
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
      

        hashed_user_password=get_password_hash(user.password)
      


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

        
        return {"casino":casino,"user":casino_user}
   except Exception as e :
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating casino+user: {str(e)}"
        )