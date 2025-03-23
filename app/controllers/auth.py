from fastapi import APIRouter, Depends, HTTPException, status
from views.auth import LoginRequest
from services.auth_service import authenticate_user, register_user
from dependancies.auth import get_current_user
from models.model import User
from views.auth import RegisterRequest
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(prefix="/auth/user", tags=["Authentication"])



@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)

@router.post("/login")
async def login(request: LoginRequest):
    token = authenticate_user(request.email, request.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return {"email": user.email, "first_name": user.first_name, "last_name":user.last_name, "created_at":user.created_at}
