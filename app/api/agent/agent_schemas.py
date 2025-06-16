from pydantic import BaseModel, Field

from app.constants.role import UserRole

class AgentCreate(BaseModel):
    username:str
    password:str
    role:UserRole=Field(default=UserRole.AGENT)

