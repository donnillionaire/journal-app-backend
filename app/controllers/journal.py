from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.model import Journal, User
from views.journal_schema import JournalCreate, JournalResponse, JournalListResponse,JournalAPIResponse
from typing import List
from utils.auth import get_current_user  # Import authentication
from uuid import UUID  # Import UUID


router = APIRouter(prefix="/api/journals", tags=["Journals"])

@router.post("/", response_model=JournalAPIResponse)
def create_journal(
    journal: JournalCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    new_journal = Journal(**journal.dict(), user_id=current_user.id)
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    # return new_journal
    return {
        "status": "success",
        "message": "Journal created successfully",
        "data": JournalResponse.model_validate(new_journal),  # ✅ Convert ORM object to Pydantic model
    }




@router.get("/", response_model=JournalListResponse)  # ✅ Use the new response model
def get_journals(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    journals = db.query(Journal).filter(Journal.user_id == current_user.id).all()
    
    return {
        "status": "success",
        "message": "Journals retrieved successfully",
        "data": [JournalResponse.model_validate(j) for j in journals],  # ✅ Convert to Pydantic model
        "total": len(journals)
    }

@router.get("/{journal_id}", response_model=JournalAPIResponse)
def get_journal(
    journal_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    return {
        "status": "success",
        "message": "Journal retrieved successfully",
        "data": JournalResponse.model_validate(journal),  # ✅ Convert ORM object to Pydantic model
    }



@router.put("/{journal_id}", response_model=JournalResponse)
def update_journal(
    journal_id: UUID, 
    journal_data: JournalCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    for key, value in journal_data.dict().items():
        setattr(journal, key, value)
    
    db.commit()
    db.refresh(journal)
    return journal

@router.delete("/{journal_id}")
def delete_journal(
    journal_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    db.delete(journal)
    db.commit()
    return {"message": "Journal deleted successfully"}
