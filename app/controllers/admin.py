from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model import User
from app.views.auth import LoginRequest, Token
from passlib.context import CryptContext
from app.utils.auth import create_access_token
from datetime import timedelta
from app.views.auth import RegisterRequest
from app.views.user_schema import UserResponse, UserAPIResponse, UserListResponse
from app.services.admin_service import login_admin, register_admin, get_all_users_service
from app.utils.auth import get_current_user

router = APIRouter(prefix="/auth/admin", tags=["Admin"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_admin(request, db)




@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_admin(request, db)


@router.get("/profile", response_model=UserAPIResponse)
async def get_profile(user: User = Depends(get_current_user)):
    return UserAPIResponse(
        status="success",
        message="Profile retrieved successfully",
        data=UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role  # Include the role in the response
        )
    )
    
    
    
@router.get("/all-users", response_model=UserListResponse)  # ✅ Use the new response model
async def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of users per page"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    
    
    print("current role", current_user.role.value)
    # Ensure the user is an admin
    # if current_user.role.value != "ADMIN":
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to access this resource"
    #     )

    # Call the service layer to retrieve users
    users_data = get_all_users_service(db, page, limit)

    return UserListResponse(
        status="success",
        message="Users retrieved successfully",
        data=users_data["data"],
        metadata=users_data["metadata"]
    )