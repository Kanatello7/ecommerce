from pydantic import BaseModel

class Token(BaseModel):
    access_token: str 
    refresh_token: str 
    token_type: str

class UserRegister(BaseModel):
    first_name: str 
    last_name: str 
    email: str 
    password: str
    password_confirm: str 

