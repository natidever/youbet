from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRETE_KEY:str
    ALGORITHM:str
    REDIS_URL:str
    model_config = SettingsConfigDict(env_file=".env")

    # class Config:
    #     env_file=".env"
