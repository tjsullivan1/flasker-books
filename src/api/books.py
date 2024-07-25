# src/api/users.py

from http import HTTPStatus

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

books_ns = Namespace("books")


class NullableString(fields.String):
    __schema_type__ = ["string", "null"]
    __schema_example__ = "nullable string"


# class NullableInt(fields.Integer):
#     __schema_type__ = ['integer', 'null']
#     __schema_example__ = 'nullable integer'


# class NullableDateTime(fields.DateTime):
#     __schema_type__ = ['string', 'null']
#     __schema_example__ = 'nullable string'


book = books_ns.model(
    "Book",
    {
        "id": fields.String(readOnly=True),
        "title": fields.String(required=True),
        "author": NullableString,
        "genre": NullableString,
        "date_added": NullableString,  # TODO: Ideally this would be a datetime
        "priority": NullableString,
        "referred_by": NullableString,
        "status": NullableString,
        "category": NullableString,
        "notes": NullableString,
        "type_read": NullableString,
        "rating": NullableString,  # TODO: Ideally this would be an integer
        "date_read": NullableString,  # TODO: Ideally this would be a datetime
    },
)


class BookList(Resource):

    @books_ns.marshal_with(book, as_list=True)
    def get(self):
        """Returns all books"""
        return get_all_books(), HTTPStatus.OK

    @books_ns.expect(book, validate=True)
    @books_ns.response(HTTPStatus.CREATED, "<title> was added!")
    @books_ns.response(HTTPStatus.CONFLICT, "Sorry. That title already exists.")
    def post(self):
        """Creates a new book."""
        post_data = request.get_json()
        title = post_data.get("title")
        author = post_data.get("author")
        response_object = {}

        book = get_book_by_title(title)
        if book:
            response_object["message"] = "Sorry. That title already exists."
            return response_object, HTTPStatus.CONFLICT

        add_book(title, author)

        response_object["message"] = f"{title} was added!"
        return response_object, HTTPStatus.CREATED


class Books(Resource):

    @books_ns.marshal_with(book)
    @books_ns.response(HTTPStatus.OK, "Success")
    @books_ns.response(HTTPStatus.NOT_FOUND, "Book <book_id> does not exist")
    def get(self, book_id):
        """Returns a single book"""
        book = get_book_by_id(book_id)
        if not book:
            books_ns.abort(HTTPStatus.NOT_FOUND, f"Book {book_id} does not exist")
        return book, HTTPStatus.OK

    @books_ns.response(HTTPStatus.OK, "<book_id> was removed!")
    @books_ns.response(HTTPStatus.NOT_FOUND, "Book <book_id> does not exist")
    def delete(self, book_id):
        """Removes a single book"""
        response_object = {}
        book = get_book_by_id(book_id)

        if not book:
            books_ns.abort(HTTPStatus.NOT_FOUND, f"Book {book_id} does not exist")

        delete_book(book)

        response_object["message"] = f"{book.title} was removed!"  # type: ignore -- we abort ahead of time with a 404 if the book does not exist, so this should never be None # noqa: E501
        return response_object, HTTPStatus.OK

    @books_ns.expect(book, validate=True)
    @books_ns.response(HTTPStatus.OK, "<book_id> was updated!")
    @books_ns.response(HTTPStatus.NOT_FOUND, "Book <book_id> does not exist")
    @books_ns.response(HTTPStatus.CONFLICT, "Sorry. That book already exists.")
    def put(self, book_id):
        """Updates a book"""
        response_object = {}

        book = get_book_by_id(book_id)
        if not book:
            books_ns.abort(HTTPStatus.NOT_FOUND, f"Book {book_id} does not exist")

        post_data = request.get_json()

        title = post_data.get("title")
        author = post_data.get("author", book.author)
        genre = post_data.get("genre", book.genre)
        priority = post_data.get("priority", book.priority)
        referred_by = post_data.get("referred_by", book.referred_by)
        status = post_data.get("status", book.status)
        category = post_data.get("category", book.category)
        notes = post_data.get("notes", book.notes)
        type_read = post_data.get("type_read", book.type_read)
        rating = post_data.get("rating", book.rating)
        date_read = post_data.get("date_read", book.date_read)

        if get_book_by_title(title):
            response_object["message"] = "Sorry. That book already exists."
            return response_object, HTTPStatus.CONFLICT

        update_book(
            book,
            title,
            author,
            genre,
            priority,
            referred_by,
            status,
            category,
            notes,
            type_read,
            rating,
            date_read,
        )

        response_object["message"] = f"{book.id} was updated!"  # type: ignore -- I think this is necessary because a NoneType should not be returned - if it were, we would catch it with the NOT_FOUND error. # noqa: E501
        return response_object, HTTPStatus.OK


books_ns.add_resource(BookList, "")
# TODO: I think that string: can be replaced with uuid:
books_ns.add_resource(Books, "/<string:book_id>")
