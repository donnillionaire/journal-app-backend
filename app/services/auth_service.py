from database import get_db
from sqlalchemy.orm import Session
from models.model import User
import jwt  # Using PyJWT
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from views.auth import RegisterRequest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.model import User
from passlib.context import CryptContext


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



def register_user(request, db: Session):
    # 🔹 Use `query()` instead of `select()`
    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)

    # Create a new user
    new_user = User(email=request.email, first_name=request.first_name, last_name=request.last_name, password=hashed_password)

    # Add the new user to the session
    db.add(new_user)
    db.commit()  # Commit changes to the database
    db.refresh(new_user)  # Refresh to get the latest state

    return {"message": "User registered successfully"}