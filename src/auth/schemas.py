from pydantic import BaseModel

class Token(BaseModel):
    access_token: str 
    refresh_token: str 
    token_type: str = 'bearer'

class UserOut(BaseModel):
    first_name: str 
    last_name: str 
    email: str

class UserRegister(UserOut):
    password: str
    password_confirm: str 

