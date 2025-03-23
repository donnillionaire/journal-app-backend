from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Odhiambo10@127.0.0.1:5432/journal"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
