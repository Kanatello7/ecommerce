from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class SettingsJWT(BaseSettings):
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int 

settings_jwt = SettingsJWT()
