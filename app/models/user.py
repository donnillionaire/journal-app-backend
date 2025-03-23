# from sqlalchemy import Column, Integer, String, DateTime, func
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.dialects.postgresql import UUID

# import uuid




# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     first_name = Column(String, index=True)
#     last_name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)
#     created_at = Column(DateTime, default=func.now())  # Corrected line
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

# Many-to-Many Association Table
journal_tags = Table(
    "journal_tags",
    Base.metadata,
    Column("journal_id", UUID(as_uuid=True), ForeignKey("journals.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())

    journals = relationship("Journal", back_populates="user", cascade="all, delete-orphan")


class Journal(Base):
    __tablename__ = "journals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="journals")
    tags = relationship("Tag", secondary=journal_tags, back_populates="journals")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    journals = relationship("Journal", secondary=journal_tags, back_populates="tags")
