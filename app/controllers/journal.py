from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.model import Journal, User
from views.journal_schema import JournalCreate, JournalResponse, JournalListResponse,JournalAPIResponse, JournalUpdate
from views.user_schema import SummaryResponse
from typing import List
from utils.auth import get_current_user  # Import authentication
from utils.journal import tokenize_and_clean 
from collections import Counter


from uuid import UUID  # Import UUID
from datetime import datetime
from sqlalchemy.types import Date  # ✅ Import Date type
from sqlalchemy.sql.expression import cast
from sqlalchemy import desc  # Import `desc` for descending order
from sqlalchemy.sql import func






router = APIRouter(prefix="/api/journals", tags=["Journals"])



@router.get("/word-frequency", response_model=dict)
def get_word_frequency(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    journals = (
        db.query(Journal)
        .filter(Journal.user_id == current_user.id)
        .all()
    )

    all_content = " ".join(journal.content for journal in journals if journal.content)

    if not all_content.strip():
        return {"word_frequency": []}

    words = tokenize_and_clean(all_content)
    word_counts = Counter(words)

    # Exclude common stop words
    stop_words = {"the", "and", "is", "in", "to", "of", "a", "for", "on", "with"}
    filtered_word_counts = {word: count for word, count in word_counts.items() if word not in stop_words}

    # Get the top 50 most common words
    top_words = sorted(filtered_word_counts.items(), key=lambda x: x[1], reverse=True)[:50]

    word_frequency = [{"text": word, "value": count} for word, count in top_words]
    return {"word_frequency": word_frequency}

@router.post("/", response_model=JournalAPIResponse)
def create_journal(
    journal: JournalCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # 🔒 Protected
):
    new_journal = Journal(**journal.model_dump(), user_id=current_user.id)
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    # return new_journal
    return {
        "status": "success",
        "message": "Journal created successfully",
        "data": JournalResponse.model_validate(new_journal),  # ✅ Convert ORM object to Pydantic model
    }




@router.get("/summaries", response_model=SummaryResponse)
def get_summaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch all journal entries for the current user
    journals = (
        db.query(Journal)
        .filter(Journal.user_id == current_user.id)
        .all()
    )

    # Compute category distribution
    category_distribution = {}
    valid_categories = ["Personal", "Work", "Travel", "Health", "Social"]
    for cat in valid_categories:
        category_distribution[cat] = 0
    for journal in journals:
        category = journal.journal_category or "Uncategorized"
        if category in category_distribution:
            category_distribution[category] += 1

    # Compute monthly counts
    monthly_counts = {}
    for journal in journals:
        month_key = journal.date_of_entry.strftime("%B %Y")
        if month_key not in monthly_counts:
            monthly_counts[month_key] = 0
        monthly_counts[month_key] += 1
    monthly_counts_list = [{"month": key, "count": value} for key, value in monthly_counts.items()]

    # Compute daily trend
    daily_trend = {}
    for journal in journals:
        day_key = journal.date_of_entry.strftime("%Y-%m-%d")
        if day_key not in daily_trend:
            daily_trend[day_key] = 0
        daily_trend[day_key] += 1
    daily_trend_list = [{"date": key, "count": value} for key, value in daily_trend.items()]
    daily_trend_list.sort(key=lambda x: x["date"])

    # Compute word count trend
    word_count_trend = {}
    for journal in journals:
        day_key = journal.date_of_entry.strftime("%Y-%m-%d")
        if day_key not in word_count_trend:
            word_count_trend[day_key] = 0
        word_count_trend[day_key] += len(journal.content.split())
    word_count_trend_list = [{"date": key, "word_count": value} for key, value in word_count_trend.items()]
    word_count_trend_list.sort(key=lambda x: x["date"])

    # Compute entry length averages by category
    entry_length_totals = {}
    entry_length_counts = {}
    for journal in journals:
        category = journal.journal_category or "Uncategorized"
        if category not in entry_length_totals:
            entry_length_totals[category] = 0
            entry_length_counts[category] = 0
        entry_length_totals[category] += len(journal.content.split())
        entry_length_counts[category] += 1

    entry_length_averages = {
        category: entry_length_totals[category] / entry_length_counts[category]
        for category in entry_length_totals
    }

    return SummaryResponse(
        category_distribution=category_distribution,
        monthly_counts=monthly_counts_list,
        daily_trend=daily_trend_list,
        word_count_trend=word_count_trend_list,
        entry_length_averages=entry_length_averages  # Include entry length averages
    )

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
    current_user: User = Depends(get_current_user)  # 🔒 
):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    # Query all journal entries for the given date and user
    journals = (
        db.query(Journal)
        .filter(Journal.user_id == current_user.id)
        .filter(func.date(Journal.date_of_entry) == target_date)  # ✅ More efficient filtering
        .order_by(desc(Journal.date_of_entry))  # Sort by `date_of_entry` in descending order (latest first)
        .all()
    )

    # Return an empty list instead of 404 if no entries exist
    journal_responses = [JournalResponse.model_validate(journal) for journal in journals]
    
    return JournalListResponse(
        status="success",
        message="Journal entries retrieved successfully" if journals else "No journal entries found",
        data=journal_responses,
        total=len(journal_responses)
    )
    
    
    



# router = APIRouter()

@router.get("/journals", response_model=JournalListResponse)
def get_journals_by_year(
    year: int = Query(..., description="The year to filter journal entries"),  # Required query parameter
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 Ensure user authentication
):
    # Validate that the year is within a reasonable range (optional but recommended)
    if year < 1900 or year > datetime.now().year:
        raise HTTPException(status_code=400, detail="Invalid year. Please provide a valid year.")

    # Query all journal entries for the user and specified year
    journals = (
        db.query(Journal)
        .filter(Journal.user_id == current_user.id)  # Filter by authenticated user
        .filter(func.extract('year', Journal.date_of_entry) == year)  # Filter by year
        .order_by(desc(Journal.date_of_entry))  # Sort by `date_of_entry` in descending order
        .all()
    )

    # Convert the query results into response objects
    journal_responses = [JournalResponse.model_validate(journal) for journal in journals]

    return JournalListResponse(
        status="success",
        message="Journal entries retrieved successfully" if journals else "No journal entries found for the specified year",
        data=journal_responses,
        total=len(journal_responses)
    )
    
    


@router.put("/{journal_id}", response_model=JournalResponse)
def update_journal(
    journal_id: UUID, 
    journal_data: JournalUpdate, 
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





@router.get("/by-category/{category}", response_model=JournalListResponse)
def get_journal_by_category(
    category: str,  # Expecting a valid category name (e.g., "Personal", "Work")
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 Ensure the user is authenticated
):
    # Validate the category (optional: you can define a list of valid categories)
    valid_categories = ["Personal", "Work", "Travel", "Health", "Social"]
    if category not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category. Choose from {', '.join(valid_categories)}.")

    # Query all journal entries for the given category and user
    journals = (
        db.query(Journal)
        .filter(Journal.user_id == current_user.id)
        .filter(Journal.journal_category == category)  # Filter by category
        .order_by(Journal.date_of_entry.desc())  # Sort by `date_of_entry` in descending order (latest first)
        .all()
    )

    # Return an empty list instead of 404 if no entries exist
    journal_responses = [JournalResponse.model_validate(journal) for journal in journals]

    return JournalListResponse(
        status="success",
        message="Journal entries retrieved successfully" if journals else "No journal entries found",
        data=journal_responses,
        total=len(journal_responses)
    )
    
    
    

