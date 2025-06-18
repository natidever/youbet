import datetime
from typing import List, Optional
from pydantic import BaseModel, Field,EmailStr
from sqlalchemy import JSON

class CasinoBase(BaseModel):
    name: str = Field(nullable=False, max_length=100)
    contact_email: Optional[EmailStr] = Field(default=None, max_length=50)
    contact_phones: List[str] = Field(default_factory=list,)
    


class UserCreate(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    username:str


class CasinoResponse(CasinoBase):
    user_id:int
    casino_id:int
    is_active:bool
    user:UserResponse
    role:str














