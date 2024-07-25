# src/api/crud.py


from datetime import datetime
from enum import Enum
from typing import Optional

from src import db
from src.models.models import Book, User


# These should be refactored with what's in models, perhaps break out into it's own file of enums for this program
class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReadingStatus(Enum):
    TO_READ = "to_read"
    READING = "reading"
    READ = "read"


class BookType(Enum):
    PHYSICAL = "physical"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, username, email):
    user.username = username
    user.email = email
    db.session.commit()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user


def get_all_books():
    return Book.query.all()


def get_book_by_id(book_id):
    return Book.query.filter_by(id=book_id).first()


def get_book_by_title(title):
    return Book.query.filter_by(title=title).first()


def add_book(title, author):
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return book


def update_book(
    book: Book,
    title: str,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    priority: Optional[PriorityLevel] = PriorityLevel.MEDIUM,
    referred_by: Optional[str] = None,
    status: Optional[ReadingStatus] = ReadingStatus.TO_READ,
    category: Optional[str] = None,
    notes: Optional[str] = None,
    type_read: Optional[BookType] = BookType.AUDIOBOOK,
    rating: Optional[int] = None,
    date_read: Optional[datetime] = None,
):
    book.title = title
    book.author = author
    book.genre = genre
    book.priority = priority
    book.referred_by = referred_by
    book.status = status
    book.category = category
    book.notes = notes
    book.type_read = type_read
    book.rating = rating
    book.date_read = date_read

    db.session.commit()
    return book


def delete_book(book):
    db.session.delete(book)
    db.session.commit()
    return book
