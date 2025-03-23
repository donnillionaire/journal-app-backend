from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt  # Using PyJWT
from models.model import User  # Adjust based on your structure
from database import get_db  # Example DB session function
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/user/login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        print("user_id", user_id)
        
        
        if not user_id:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user
