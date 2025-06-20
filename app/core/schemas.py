from typing import Optional
from pydantic import BaseModel


class RoundCreate(BaseModel):
    round_number:int
    commitment_hash:str
    server_seed:str
    state:str


    