from src.auth.utils import hash_password, verify_password, get_utc_now
from src.auth.schemas import *
from src.auth.config import settings_jwt 
from src.auth.models import User
from src.auth.repository import AuthRepository, UserRepository
from src.auth.exceptions import *

from datetime import timedelta
import jwt 

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def get_user_by_username(self, username: str) -> User:
        return await self.repository.find_one_or_more(email=username)

    async def create_new_user(self, data: dict) -> User:
        return await self.repository.create(data)
    

    # async def get_current_user(self, token: TokenDep):
    #     user = await self.get_user_by_username(user_username)
    #     return user
    
class AuthService:
    def __init__(self, repository: AuthRepository, user_service: UserService):
        self.repository = repository
        self.user_service = user_service


    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_service.get_user_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user 

    async def create_access_token(self, user: User):
        payload = {"sub": user.email,
                   "type": "access",
                   "iat": get_utc_now(), 
                   "exp": get_utc_now() + timedelta(minutes=settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)}
        
        access_token = jwt.encode(payload, settings_jwt.SECRET_KEY, algorithm=settings_jwt.ALGORITHM)
        return access_token
    
    async def create_refresh_token(self, user: User):
        payload = {"sub": user.email,
                   "type": "refresh",
                   "iat": get_utc_now(), 
                   "exp": get_utc_now() + timedelta(days=settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS)}
        
        refresh_token = jwt.encode(payload, settings_jwt.SECRET_KEY, algorithm=settings_jwt.ALGORITHM)
        return refresh_token
    
    async def create_token_pair(self, user: User):
        access_token = await self.create_access_token(user)
        refresh_token = await self.create_refresh_token(user)

        return Token(access_token=access_token, refresh_token=refresh_token, token_type='bearer')
    
    async def register_new_user(self, new_user: UserRegister):
        user_exists = await self.user_service.get_user_by_username(new_user.email)
        if user_exists:
            raise UserExistsException
        
        if new_user.password != new_user.password_confirm:
            raise PasswordDoesNotMatchException
        
        data = new_user.model_dump(exclude=["password_confirm"])
        data["password"] = hash_password(data["password"])
        user = await self.user_service.create_new_user(data)
        return user 

    async def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, settings_jwt.SECRET_KEY, algorithms=[settings_jwt.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except Exception:
            raise InvalidTokenException
        return payload
    
    async def refresh_token(self, token: str) -> Token:
        payload = await self.decode_token(token)
        username = payload.get("sub")
        if not username:
            raise InvalidTokenException
        
        user = await self.user_service.get_user_by_username(username)
        return await self.create_token_pair(user)
    