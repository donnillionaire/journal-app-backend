from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.model import User
from views.auth import LoginRequest, Token
from passlib.context import CryptContext
from utils.auth import create_access_token
from datetime import timedelta
from views.auth import RegisterRequest
from views.user_schema import UserResponse, UserAPIResponse
from services.auth_service import login_user, register_user
from utils.auth import get_current_user

router = APIRouter(prefix="/auth/user", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)




@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)


@router.get("/profile", response_model=UserAPIResponse)
async def get_profile(user: User = Depends(get_current_user)):
    return UserAPIResponse(
        status="success",
        message="User profile retrieved successfully",
        data=UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
    )