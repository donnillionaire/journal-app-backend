from app.database import get_db
from sqlalchemy.orm import Session
from app.models.model import User
import jwt  # Using PyJWT
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.views.auth import RegisterRequest

from app.views.user_schema import UserResponse


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import User, UserRole
from passlib.context import CryptContext
from app.utils.auth import create_access_token
from app.views.auth import Token, LoginRequest, LoginResponse
from typing import Dict, List



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(email: str, password: str) -> str | None:
    db = next(get_db())  # Get DB session
    user = db.query(User).filter(User.email == email).first()

    if not user or not pwd_context.verify(password, user.password):
        return None  # Invalid credentials

    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.id),  # Ensure user ID is a string for JWT compatibility
        "exp": datetime.utcnow() + access_token_expires
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token



def register_admin(request: RegisterRequest, db: Session) -> dict:
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    print("existing user", existing_user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)

    # Create a new admin user
    new_admin = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=hashed_password,
        role=UserRole.ADMIN  # Set role explicitly
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "Admin registered successfully"}








def login_admin(request: LoginRequest, db: Session) -> Token:
    # Check if user exists
    user = db.query(User.id, User.password, User.role).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verify password
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Validate role
    if user.role.value != UserRole.ADMIN.value:  # Use constants for roles
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # Generate access token
    access_token = create_access_token(
        data={"sub": str(user.id)},  # User ID is included in the token payload
        role=user.role.value,       # Role is passed as a separate argument
        expires_delta=timedelta(minutes=30)
    )
    
    
    data=LoginResponse(
            token=access_token,
            role=user.role.value
          
        )

    return data


def get_all_users_service(db: Session, page: int, limit: int) -> Dict:
    # Calculate pagination indices
    offset = (page - 1) * limit

    # Query the database for users
    users_query = db.query(User).offset(offset).limit(limit)
    total_users = db.query(User).count()  # Total number of users for pagination metadata
    users = users_query.all()

    # Format the response data
    user_list = [
        UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role
        )
        for user in users
    ]

    return {
        "data": user_list,
        "metadata": {
            "page": page,
            "limit": limit,
            "total_users": total_users
        }
    }