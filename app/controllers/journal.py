from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.model import Journal, User
from views.journal_schema import JournalCreate, JournalResponse
from typing import List
from utils.auth import get_current_user  # Import authentication

router = APIRouter(prefix="/api/journals", tags=["Journals"])

@router.post("/", response_model=JournalResponse)
def create_journal(
    journal: JournalCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    new_journal = Journal(**journal.dict(), user_id=current_user.id)
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return new_journal

@router.get("/", response_model=List[JournalResponse])
def get_journals(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    return db.query(Journal).filter(Journal.user_id == current_user.id).all()

@router.get("/{journal_id}", response_model=JournalResponse)
def get_journal(
    journal_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal

@router.put("/{journal_id}", response_model=JournalResponse)
def update_journal(
    journal_id: int, 
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
    journal_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    db.delete(journal)
    db.commit()
    return {"message": "Journal deleted successfully"}
