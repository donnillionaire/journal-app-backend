# from fastapi import APIRouter, Depends, HTTPException, status
# from views.auth import LoginRequest
# from services.auth_service import authenticate_user, register_user
# from dependancies.auth import get_current_user
# from models.model import User
# from views.auth import RegisterRequest
# from sqlalchemy.orm import Session
# from database import get_db


# router = APIRouter(prefix="/auth/user", tags=["Authentication"])



# @router.post("/register", status_code=status.HTTP_201_CREATED)
# def register(request: RegisterRequest, db: Session = Depends(get_db)):
#     return register_user(request, db)

# @router.post("/login")
# async def login(request: LoginRequest):
#     token = authenticate_user(request.email, request.password)
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     return {"access_token": token, "token_type": "bearer"}

# @router.get("/profile")
# async def get_profile(user: User = Depends(get_current_user)):
#     return {"email": user.email, "first_name": user.first_name, "last_name":user.last_name, "created_at":user.created_at}





from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.model import User
from views.auth import LoginRequest, Token
from passlib.context import CryptContext
from utils.auth import create_access_token
from datetime import timedelta
from views.auth import RegisterRequest
from services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth/user", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)




@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)

# @router.post("/login", response_model=Token)
# def login(request: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == request.email).first()
#     if not user or not pwd_context.verify(request.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     access_token = create_access_token(
#         data={"sub": user.id}, 
#         expires_delta=timedelta(minutes=30)  # Token expires in 30 minutes
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
