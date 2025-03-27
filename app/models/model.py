# from sqlalchemy import Column, Integer, String, DateTime, func
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.dialects.postgresql import UUID

# import uuid




from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid
from sqlalchemy.orm import validates
from datetime import datetime
import enum



Base = declarative_base()

# Many-to-Many Association Table
# journal_tags = Table(
#     "journal_tags",
#     Base.metadata,
#     Column("journal_id", UUID(as_uuid=True), ForeignKey("journals.id"), primary_key=True),
#     Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
# )



class Journal(Base):
    __tablename__ = "journals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    journal_category = Column(String, nullable=False)
    date_of_entry = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="journals")

    @validates("date_of_entry")
    def validate_date(self, key, date):
        if date > datetime.now():
            raise ValueError("date_of_entry cannot be in the future.")
        return date


# Define role types
class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"   
    
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    role = Column(Enum(UserRole, name="userrole"), nullable=False, default=UserRole.USER)

    journals = relationship("Journal", back_populates="user", cascade="all, delete-orphan")



