from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.schemas import *
from src.auth.service import AuthService

from typing import Annotated

router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),):
    user = AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthService.create_token_pair(user)
    

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(new_user: UserRegister):
    AuthService.register_new_user(new_user)
    

@router.post("/logout")
def logout(token: Annotated[str,Depends(oauth2_scheme)]):
    AuthService.logout(token)
    return {"meessage": "Log out successfully"}    