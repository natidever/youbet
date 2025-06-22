from pydantic import BaseModel


class AuthSchema(BaseModel):
    password:str
    username:str



class AuthSchemaPost(BaseModel):
    role:str
    username:str
    user_id:int
    is_active:bool
    access_token:str
    casino_id:int | None = None
    



