from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.model import Journal
from views.journal_schema import JournalCreate, JournalResponse
from typing import List

router = APIRouter(prefix="/journals", tags=["Journals"])

# Create a journal entry
@router.post("/", response_model=JournalResponse)
def create_journal(journal: JournalCreate, db: Session = Depends(get_db)):
    new_journal = Journal(**journal.dict())
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return new_journal

# Get all journal entries
@router.get("/", response_model=List[JournalResponse])
def get_journals(db: Session = Depends(get_db)):
    return db.query(Journal).all()

# Get a single journal entry by ID
@router.get("/{journal_id}", response_model=JournalResponse)
def get_journal(journal_id: int, db: Session = Depends(get_db)):
    journal = db.query(Journal).filter(Journal.id == journal_id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal

# Update a journal entry
@router.put("/{journal_id}", response_model=JournalResponse)
def update_journal(journal_id: int, journal_data: JournalCreate, db: Session = Depends(get_db)):
    journal = db.query(Journal).filter(Journal.id == journal_id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    
    for key, value in journal_data.dict().items():
        setattr(journal, key, value)
    
    db.commit()
    db.refresh(journal)
    return journal

# Delete a journal entry
@router.delete("/{journal_id}")
def delete_journal(journal_id: int, db: Session = Depends(get_db)):
    journal = db.query(Journal).filter(Journal.id == journal_id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    db.delete(journal)
    db.commit()
    return {"message": "Journal deleted successfully"}
