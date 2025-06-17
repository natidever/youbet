
from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.api.agent.agent_schemas import AgentCreate
from app.config.db import get_session
from app.constants.role import UserRole
from app.models.core_models import User

def register_agnet(agnet:AgentCreate,session:Session):
   
   try:
    agnet_object = User(
        username=agnet.username,
        password_hash=agnet.password,
        role=UserRole.AGENT

    )
    session.add(agnet_object)
    session.commit()
    session.refresh(agnet_object)
    return agnet
   except Exception as e :
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating agent: {str(e)}"
        )