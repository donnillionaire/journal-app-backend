from pydantic import BaseModel, EmailStr
from uuid import UUID  # Import UUID
from typing import List, Dict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Include password for user creation



class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role : str

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
    word_count_trend: List[dict]
    entry_length_averages: Dict[str, float]  # Add entry length averages



from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class UserResponse(BaseModel):
    id:UUID
    first_name: str
    last_name: str
    email: str
    role: str

class Metadata(BaseModel):
    page: int
    limit: int
    total_users: int

class UserListResponse(BaseModel):
    status: str
    message: str
    data: List[UserResponse]
    metadata: Metadata