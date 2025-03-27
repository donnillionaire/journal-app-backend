class JournalResponse(JournalCreate):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes =True


# ✅ New response model to match your return structure
class JournalListResponse(BaseModel):
    status: str
    message: str
    data: List[JournalResponse]  # List of journals
    total: int