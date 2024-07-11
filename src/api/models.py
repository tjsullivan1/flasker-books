# src/api/models.py

from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Text,
    String,
    DateTime,
    Enum as SQLEnum,
    CheckConstraint,
    Integer,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src import db


class User(db.Model):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    active = Column(Boolean(), default=True, nullable=False)
    created_date = Column(DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class PriorityLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReadingStatus(Enum):
    TO_READ = "to_read"
    READING = "reading"
    READ = "read"


class BookType(Enum):
    PHYSICAL = "physical"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"


class Book(db.Model):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(Text)
    author = Column(Text)
    genre = Column(Text)
    date_added = Column(DateTime, default=func.now())
    priority = Column(SQLEnum(PriorityLevel), default=PriorityLevel.LOW, nullable=False)
    referred_by = Column(Text)
    status = Column(
        SQLEnum(ReadingStatus), default=ReadingStatus.TO_READ, nullable=False
    )
    category = Column(Text)
    notes = Column(Text)
    type_read = Column(SQLEnum(BookType), default=BookType.AUDIOBOOK, nullable=False)
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 5"))
    date_read = Column(DateTime)

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range"),
    )

    def __init__(self, title, author):
        self.title = title
        self.author = author
