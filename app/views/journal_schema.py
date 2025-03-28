from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List
from app.models.model import Journal
from typing import Optional

class JournalCreate(BaseModel):
    title: str
    content: str
    date_of_entry: datetime  # ✅ Now Pydantic will parse it automatically
    journal_category: str
    
    
    
class JournalUpdate(BaseModel):
    title: str
    content: str
    # sentiment: str
    journal_category: str


class JournalResponse(JournalCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
    sentiment: Optional[str] = None  # ✅ Sentiment is included but NOT required

    class Config:
        orm_mode = True
        from_attributes =True


# ✅ New response model to match your return structure
class JournalListResponse(BaseModel):
    status: str
    message: str
    data: List[JournalResponse]  # List of journals
    total: int



class JournalAPIResponse(BaseModel):
    status: str
    message: str
    data: JournalResponse  # List of journals
    
