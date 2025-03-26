from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.model import Journal, User
from views.journal_schema import JournalCreate, JournalResponse, JournalListResponse,JournalAPIResponse
from typing import List
from utils.auth import get_current_user  # Import authentication
from uuid import UUID  # Import UUID
from datetime import datetime
from sqlalchemy.types import Date  # ✅ Import Date type
from sqlalchemy.sql.expression import cast





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
    
    
    


@router.get("/by-date/{date}", response_model=JournalListResponse)
def get_journal_by_date(
    date: str,  # Expecting YYYY-MM-DD format
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Query all journal entries for the given date and user
    journals = (
        db.query(Journal)
        .filter(Journal.user_id == current_user.id)
        .filter(cast(Journal.created_at, Date) == target_date)  # ✅ Explicitly cast `created_at` to Date
        .all()  # Retrieve all matching entries
    )

    if not journals:
        raise HTTPException(status_code=404, detail="No journal entries found for the given date")

    # Validate and convert each journal entry into the JournalResponse schema
    journal_responses = [JournalResponse.model_validate(journal) for journal in journals]

    # Return the response with the total count of entries
    return JournalListResponse(
        status="success",
        message="Journal entries retrieved successfully",
        data=journal_responses,
        total=len(journal_responses)  # Total number of entries
    )
    



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
