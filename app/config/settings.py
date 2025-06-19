from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRETE_KEY:str
    ALGORITHM:str
    REDIS_URL:str

    class Config:
        env_file=".env"
