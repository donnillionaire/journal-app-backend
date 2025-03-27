from pydantic import BaseModel, EmailStr
from uuid import UUID  # Import UUID
from typing import List


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Include password for user creation





class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True




class UserAPIResponse(BaseModel):
    status: str
    message: str
    data: UserResponse  # List of journals
    
    
    
class SummaryResponse(BaseModel):
    category_distribution: dict
    monthly_counts: List[dict]
    daily_trend: List[dict]
    word_count_trend: List[dict]  # Add word count trend
