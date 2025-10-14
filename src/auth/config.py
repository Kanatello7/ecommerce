from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class SettingsJWT(BaseSettings):
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: str 
    REFRESH_TOKEN_EXPIRE_DAYS: str 

settings_jwt = SettingsJWT()
