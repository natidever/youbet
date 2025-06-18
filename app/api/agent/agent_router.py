from fastapi import Depends, FastAPI,APIRouter

from app.api.agent.agent_schemas import AgentCreate
from app.config.db import get_session
from app.constants.role import UserRole
from app.dependencies.auth_dependecies import require_role
from app.api.agent.agent_services import register_agnet

agent_router =APIRouter(tags=["Agent"])

@agent_router.post("/register-agent/")
async def register_agent(
                        agent_data:AgentCreate,
                        role=Depends(require_role([UserRole.ADMIN])),
                        session=Depends(get_session),

                    
                       ):
   return  register_agnet(agnet=agent_data,session=session)

