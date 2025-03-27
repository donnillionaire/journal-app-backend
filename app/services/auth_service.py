from app.database import get_db
from sqlalchemy.orm import Session
from app.models.model import User
import jwt  # Using PyJWT
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.views.auth import RegisterRequest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import User
from passlib.context import CryptContext
from app.utils.auth import create_access_token
from app.views.auth import Token, LoginRequest, LoginResponse


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



def register_user(request: RegisterRequest, db: Session) -> Token:
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)

    # Create a new user
    new_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate access token
    access_token = create_access_token(
        data={"sub": str(new_user.id)},
        expires_delta=timedelta(minutes=30)
    )

    # return {"access_token": access_token, "token_type": "bearer"}

    return {"message": "User registered successfully"}



def login_user(request: LoginRequest, db: Session) -> Token:
    # Check if user exists
    user = db.query(User.id, User.password, User.role).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verify password
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

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

    