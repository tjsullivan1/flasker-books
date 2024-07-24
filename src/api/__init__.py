# src/api/__init__.py

from flask_restx import Api

from src.api.books import books_namespace
from src.api.ping import ping_namespace
from src.api.users import users_namespace

api = Api(version="1.0", title="My API", doc="/docs")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(users_namespace, path="/api/users")
api.add_namespace(books_namespace, path="/api/books")
