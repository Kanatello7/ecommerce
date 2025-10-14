from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import UserLogin
from utils import *

router = APIRouter(tags=["auth"])

@router.post("/login")
def login(creds: UserLogin):
    pass 