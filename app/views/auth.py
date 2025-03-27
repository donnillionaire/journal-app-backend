from pydantic import BaseModel, EmailStr
from app.models.model import User
class LoginRequest(BaseModel):
    email: EmailStr
    password: str




# Registration function
class RegisterRequest(BaseModel):
    email: str
    first_name: str
    last_name : str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    

class LoginResponse(BaseModel):
    token: str
    role: str
   