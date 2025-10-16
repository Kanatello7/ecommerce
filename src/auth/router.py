from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src.auth.schemas import *
from src.auth.exceptions import InvalidCredentialsException
from src.auth.dependencies import AuthServiceDep
from src.auth.config import settings_jwt

from typing import Annotated

router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

@router.post("/login", response_model=Token)
async def login(response: Response, service: AuthServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsException
    token = await service.create_token_pair(user)
    response.set_cookie(
        'access_token',
        token.access_token,
        max_age=settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True
    )
    return token

@router.post('/refresh')
async def refresh_token(request: Request, response: Response, service: AuthServiceDep):
    refresh_token = request.cookies.get("refresh_token")
    token = await service.refresh_token(refresh_token)
    response.set_cookie(
        'access_token',
        token.access_token,
        max_age=settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True
    )
    return token 

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(service: AuthServiceDep, new_user: UserRegister):
    await service.register_new_user(new_user=new_user)
    
@router.post("/logout")
async def logout(response: Response, service: AuthServiceDep):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    
    return {"message": "Logged out successfully"}   