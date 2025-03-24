from pydantic import BaseModel, EmailStr

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