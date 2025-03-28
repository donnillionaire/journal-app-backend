from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.model import Base
import os

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Odhiambo10@127.0.0.1:5432/journal"
SQLALCHEMY_DATABASE_URL = os.getenv("REMOTE_DATABASE_URL")  # Use an environment variable for security

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
