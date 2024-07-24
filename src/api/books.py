# src/api/users.py


from flask import request
from flask_restx import Namespace, Resource, fields

from src import db  # noqa: F401
from src.models.models import Book  # noqa: F401

from src.api.crud import (  # isort:skip
    get_all_books,
    get_book_by_id,
    get_book_by_title,
    add_book,
    update_book,
    delete_book,
)

books_namespace = Namespace("books")


book = books_namespace.model(
    "Book",
    {
        "id": fields.String(readOnly=True),
        "title": fields.String(required=True),
        "author": fields.String,
        "genre": fields.String,
        "date_added": fields.DateTime,
        "priority": fields.String,
        "referred_by": fields.String,
        "status": fields.String,
        "category": fields.String,
        "notes": fields.String,
        "type_read": fields.String,
        "rating": fields.Integer,
        "date_read": fields.DateTime,
    },
)


class BookList(Resource):

    @books_namespace.marshal_with(book, as_list=True)
    def get(self):
        """Returns all books"""
        return get_all_books(), 200

    @books_namespace.expect(book, validate=True)
    @books_namespace.response(201, "<title> was added!")
    @books_namespace.response(400, "Sorry. That title already exists.")
    def post(self):
        """Creates a new book."""
        post_data = request.get_json()
        title = post_data.get("title")
        author = post_data.get("author")
        response_object = {}

        book = get_book_by_title(title)
        if book:
            response_object["message"] = "Sorry. That title already exists."
            return response_object, 400

        add_book(title, author)

        response_object["message"] = f"{title} was added!"
        return response_object, 201


class Books(Resource):

    @books_namespace.marshal_with(book)
    @books_namespace.response(200, "Success")
    @books_namespace.response(404, "Book <book_id> does not exist")
    def get(self, book_id):
        """Returns a single book"""
        book = get_book_by_id(book_id)
        if not book:
            books_namespace.abort(404, f"Book {book_id} does not exist")
        return book, 200

    @books_namespace.response(200, "<book_id> was removed!")
    @books_namespace.response(404, "Book <book_id> does not exist")
    def delete(self, book_id):
        """Removes a single book"""
        response_object = {}
        book = get_book_by_id(book_id)

        if not book:
            books_namespace.abort(404, f"Book {book_id} does not exist")

        delete_book(book)

        response_object["message"] = f"{book.title} was removed!"
        return response_object, 200

    @books_namespace.expect(book, validate=True)
    @books_namespace.response(200, "<book_id> was updated!")
    @books_namespace.response(404, "Book <book_id> does not exist")
    @books_namespace.response(400, "Sorry. That book already exists.")
    def put(self, book_id):
        """Updates a book"""
        post_data = request.get_json()
        author = post_data.get("author")
        title = post_data.get("title")
        response_object = {}

        book = get_book_by_id(book_id)
        if not book:
            books_namespace.abort(404, f"Book {book_id} does not exist")

        if get_book_by_title(title):
            response_object["message"] = "Sorry. That book already exists."
            return response_object, 400

        update_book(book, title, author)

        response_object["message"] = f"{book.id} was updated!"
        return response_object, 200


books_namespace.add_resource(BookList, "")
# TODO: I think that string: can be replaced with uuid:
books_namespace.add_resource(Books, "/<string:book_id>")
