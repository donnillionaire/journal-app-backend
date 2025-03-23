from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class JournalCreate(BaseModel):
    title: str
    content: str

class JournalResponse(JournalCreate):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
