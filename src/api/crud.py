# src/api/crud.py


from src import db
from src.api.models import User, Book


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


def update_book(book, title, author):
    book.title = title
    book.author = author
    db.session.commit()
    return book


def delete_book(book):
    db.session.delete(book)
    db.session.commit()
    return book
