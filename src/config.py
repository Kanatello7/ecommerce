from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class SettingsDB(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str 
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return "postgresql+asyncpg://postgres:postgres@localhost:5432/ecommerce"
    

settings_db = SettingsDB()


