import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import JSON


class CasinoBase(BaseModel):
    name: str = Field(nullable=False, max_length=100)
    contact_email: Optional[str] = Field(default=None, max_length=12)
    contact_phones: List[str] = Field(default_factory=list,)
    

class CasinoResponse(CasinoBase):
    id:int

class UserCreate(BaseModel):
    username:str
    password:str



