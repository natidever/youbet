import datetime
from typing import List, Optional
from pydantic import BaseModel, Field,EmailStr
from sqlalchemy import JSON

class CasinoBase(BaseModel):
    name: str = Field(json_schema_extra={"nullable": False} , max_length=100)
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















class TicketBase(BaseModel):
    guessed_multiplier: float = Field(nullable=False, description="The multiplier guessed by the player",ge=1)
    bet_amount: float = Field(nullable=False, ge=20,description="bet amount should be atleaset 20")

 



class TicketCreate(TicketBase):
    pass
   




class TicketResponse(TicketBase):
    id:int
    ticket_code: str = Field(nullable=False, description="Printed code for validation")
    payout_amount: Optional[float] = Field(default=None, ge=0, description="Amount to pay out if winner")
    round_id: int





 



































