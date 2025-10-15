from src.auth.utils import hash_password, verify_password, get_utc_now
from src.auth.schemas import *
from src.auth.config import settings_jwt 
from src.auth.models import User

from datetime import timedelta
import jwt 


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.repository.get_user_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user 

    async def create_access_token(self, user: User):
        payload = {"sub": user.email,
                   "iat": get_utc_now(), 
                   "exp": get_utc_now() + timedelta(minutes=settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)}
        
        access_token = jwt.encode(payload, settings_jwt.SECRET_KEY, algorithm=settings_jwt.ALGORITHM)
        return access_token
    
    async def create_refresh_token(self, user: User):
        payload = {"sub": user.email,
                   "iat": get_utc_now(), 
                   "exp": get_utc_now() + timedelta(days=settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS)}
        
        refresh_token = jwt.encode(payload, settings_jwt.SECRET_KEY, algorithm=settings_jwt.ALGORITHM)
        return refresh_token
    
    async def create_token_pair(self, user: User):
        access_token = await self.create_access_token(user)
        refresh_token = await self.create_refresh_token(user)

        return Token(access_token=access_token, refresh_token=refresh_token, token_type='bearer')
    
    async def register_new_user(self, new_user: UserRegister):
        user = self.repository.get_user_by_username(new_user.email)

class UserService:
    def __init__(self, repository):
        self.repository = repository
    
    async def 
    