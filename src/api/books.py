# src/api/users.py


from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import Book


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

        book = Book.query.filter_by(title=title).first()
        if book:
            response_object["message"] = "Sorry. That title already exists."
            return response_object, 400

        db.session.add(Book(title=title, author=author))
        db.session.commit()

        response_object["message"] = f"{title} was added!"
        return response_object, 201

    @api.marshal_with(book, as_list=True)
    def get(self):
        return Book.query.all(), 200


class Books(Resource):

    @api.marshal_with(book)
    def get(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            api.abort(404, f"Book {book_id} does not exist")
        return book, 200


api.add_resource(BookList, "/books")
api.add_resource(Books, "/books/<string:book_id>")
