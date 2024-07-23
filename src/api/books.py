# src/api/users.py


from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from src import db  # noqa: F401
from src.api.models import Book  # noqa: F401

from src.api.crud import (  # isort:skip
    get_all_books,
    get_book_by_id,
    get_book_by_title,
    add_book,
    update_book,
    delete_book,
)

books_blueprint = Blueprint("books", __name__)
api = Api(books_blueprint)


book = api.model(
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

    @api.expect(book, validate=True)
    def post(self):
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

    @api.marshal_with(book, as_list=True)
    def get(self):
        return get_all_books(), 200


class Books(Resource):

    @api.marshal_with(book)
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if not book:
            api.abort(404, f"Book {book_id} does not exist")
        return book, 200

    def delete(self, book_id):
        response_object = {}
        book = get_book_by_id(book_id)

        if not book:
            api.abort(404, f"Book {book_id} does not exist")

        delete_book(book)

        response_object["message"] = f"{book.title} was removed!"
        return response_object, 200

    @api.expect(book, validate=True)
    def put(self, book_id):
        post_data = request.get_json()
        author = post_data.get("author")
        title = post_data.get("title")
        response_object = {}

        book = get_book_by_id(book_id)
        if not book:
            api.abort(404, f"Book {book_id} does not exist")

        if get_book_by_title(title):
            response_object["message"] = "Sorry. That book already exists."
            return response_object, 400

        update_book(book, title, author)

        response_object["message"] = f"{book.id} was updated!"
        return response_object, 200


api.add_resource(BookList, "/books")
api.add_resource(Books, "/books/<string:book_id>")
