# src/tests/test_books.py


import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.api.models import Book


def test_add_book(test_app: Flask, test_database: SQLAlchemy):
    client = test_app.test_client()
    resp = client.post(
        "/books",
        data=json.dumps(
            {"title": "The Omnivore's Dilemma", "author": "Michael Pollan"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "The Omnivore's Dilemma was added!" in data["message"]


def test_add_user_invalid_json(test_app: Flask, test_database: SQLAlchemy):
    client = test_app.test_client()
    resp = client.post(
        "/books",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_book_invalid_json_keys(test_app: Flask, test_database: SQLAlchemy):
    client = test_app.test_client()
    resp = client.post(
        "/books",
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_book_duplicate_title(test_app: Flask, test_database: SQLAlchemy):
    client = test_app.test_client()
    client.post(
        "/books",
        data=json.dumps(
            {"title": "The Omnivore's Dilemma", "author": "Michael Pollan"}
        ),
        content_type="application/json",
    )
    resp = client.post(
        "/books",
        data=json.dumps(
            {"title": "The Omnivore's Dilemma", "author": "Michael Pollan"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That title already exists." in data["message"]


def test_single_book(test_app, test_database, add_book):
    book = add_book(title="jeffrey", author="jeffrey@testdriven.io")
    client = test_app.test_client()
    resp = client.get(f"/books/{book.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "jeffrey" in data["title"]
    assert "jeffrey@testdriven.io" in data["author"]


def test_single_book_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/books/0787133b-cb55-4a31-9480-1e04b7b72898")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Book 0787133b-cb55-4a31-9480-1e04b7b72898 does not exist" in data["message"]


def test_all_books(test_app, test_database, add_book):
    test_database.session.query(Book).delete()
    add_book("The Omnivore's Dilemma", "Michael Pollan")
    add_book("The Obstacle is the Way", "Ryan Holliday")
    client = test_app.test_client()
    resp = client.get("/books")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "The Omnivore's Dilemma" in data[0]["title"]
    assert "Michael Pollan" in data[0]["author"]
    assert "The Obstacle is the Way" in data[1]["title"]
    assert "Ryan Holliday" in data[1]["author"]
