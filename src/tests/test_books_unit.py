# src/tests/test_books_unit.py


import json
from datetime import datetime

import pytest

import src.api.books


def test_add_book(test_app, monkeypatch):
    def mock_get_book_by_title(author):
        return None
    def mock_add_book(title, author):
        return True
    monkeypatch.setattr(src.api.books, "get_book_by_title", mock_get_book_by_title)
    monkeypatch.setattr(src.api.books, "add_book", mock_add_book)

    client = test_app.test_client()
    resp = client.post(
        "/books",
        data=json.dumps({"title": "Cooked", "author": "Michael Pollan"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Cooked was added!" in data["message"]


def test_add_book_invalid_json(test_app):
    client = test_app.test_client()
    resp = client.post("/books", data=json.dumps({}), content_type="application/json",)
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_book_invalid_json_keys(test_app, monkeypatch):
    client = test_app.test_client()
    resp = client.post(
        "/books",
        data=json.dumps({"author": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_book_duplicate_title(test_app, monkeypatch):
    def mock_get_book_by_title(title):
        return True 
    def mock_add_book(title, author):
        return True
    monkeypatch.setattr(src.api.books, "get_book_by_title", mock_get_book_by_title)
    monkeypatch.setattr(src.api.books, "add_book", mock_add_book)
    client = test_app.test_client()
    resp1 = client.post(
        "/books",
        data=json.dumps(
            {"title": "Cooked", "author": "Michael Pollan"}
        ),
        content_type="application/json",
    )

    data1 = json.loads(resp1.data.decode())
    print(data1)
    resp2 = client.post(
        "/books",
        data=json.dumps(
            {"title": "Cooked", "author": "Michael Pollan"}
        ),
        content_type="application/json",
    )
    data2 = json.loads(resp2.data.decode())
    print(data2)
    assert resp2.status_code == 400
    assert "Sorry. That title already exists." in data2["message"]


def test_single_book(test_app, monkeypatch):
    def mock_get_book_by_id(book_id):
        return {
            "id": "0787133b-cb55-4a31-9480-1e04b7b72898",
            "title": "jeffrey",
            "author": "jeffrey@testdriven.io",
            "created_date": datetime.now()
        }
    monkeypatch.setattr(src.api.books, "get_book_by_id", mock_get_book_by_id)
    client = test_app.test_client()
    resp = client.get("/books/0787133b-cb55-4a31-9480-1e04b7b72898")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "jeffrey" in data["title"]
    assert "jeffrey@testdriven.io" in data["author"]


def test_single_book_incorrect_id(test_app, monkeypatch):
    def mock_get_book_by_id(book_id):
        return None
    monkeypatch.setattr(src.api.books, "get_book_by_id", mock_get_book_by_id)
    client = test_app.test_client()
    resp = client.get("/books/0787133b-cb55-4a31-9480-1e04b7b72898")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Book 0787133b-cb55-4a31-9480-1e04b7b72898 does not exist" in data["message"]


def test_all_books(test_app, monkeypatch):
    def mock_get_all_books():
        return [
            {
                "id": "0787133b-cb55-4a31-9480-1e04b7b72898",
                "title": "michael",
                "author": "michael@mherman.org",
                "created_date": datetime.now()
            },
            {
                "id": "0787133b-cb55-4a31-9480-1e04b7b72899",
                "title": "fletcher",
                "author": "fletcher@notreal.com",
                "created_date": datetime.now()
            }
        ]
    monkeypatch.setattr(src.api.books, "get_all_books", mock_get_all_books)
    client = test_app.test_client()
    resp = client.get("/books")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["title"]
    assert "michael@mherman.org" in data[0]["author"]
    assert "fletcher" in data[1]["title"]
    assert "fletcher@notreal.com" in data[1]["author"]


def test_remove_book(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self
    def mock_get_book_by_id(book_id):
        d = AttrDict()
        d.update({
            "id": "0787133b-cb55-4a31-9480-1e04b7b72898",
            "title": "book-to-be-removed",
            "author": "remove-me@testdriven.io"
        })
        return d
    def mock_delete_book(book):
        return True
    monkeypatch.setattr(src.api.books, "get_book_by_id", mock_get_book_by_id)
    monkeypatch.setattr(src.api.books, "delete_book", mock_delete_book)
    client = test_app.test_client()
    resp_two = client.delete("/books/0787133b-cb55-4a31-9480-1e04b7b72898")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "book-to-be-removed was removed!" in data["message"]


def test_remove_book_incorrect_id(test_app, monkeypatch):
    def mock_get_book_by_id(book_id):
        return None
    monkeypatch.setattr(src.api.books, "get_book_by_id", mock_get_book_by_id)
    client = test_app.test_client()
    resp = client.delete("/books/0787133b-cb55-4a31-9480-1e04b7b72898")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Book 0787133b-cb55-4a31-9480-1e04b7b72898 does not exist" in data["message"]


def test_update_book(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self
    def mock_get_book_by_id(book_id):
        d = AttrDict()
        d.update({
            "id": "0787133b-cb55-4a31-9480-1e04b7b72898",
            "title": "me",
            "author": "me@testdriven.io"
        })
        return d
    def mock_update_book(book, title, author):
        return True
    def mock_get_book_by_title(title):
        return None
    monkeypatch.setattr(src.api.books, "get_book_by_id", mock_get_book_by_id)
    monkeypatch.setattr(src.api.books, "get_book_by_title", mock_get_book_by_title)
    monkeypatch.setattr(src.api.books, "update_book", mock_update_book)
    client = test_app.test_client()
    resp_one = client.put(
        "/books/0787133b-cb55-4a31-9480-1e04b7b72898",
        data=json.dumps({"title": "me", "author": "me@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert "0787133b-cb55-4a31-9480-1e04b7b72898 was updated!" in data["message"]
    resp_two = client.get("/books/0787133b-cb55-4a31-9480-1e04b7b72898")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "me" in data["title"]
    assert "me@testdriven.io" in data["author"]


@pytest.mark.parametrize(
    "book_id, payload, status_code, message",
    [
        [
            "0787133b-cb55-4a31-9480-1e04b7b72899",
            {},
            400,
            "Input payload validation failed",
        ],
        [
            "0787133b-cb55-4a31-9480-1e04b7b72897",
            {"tite": "Invalid Title"},
            400,
            "Input payload validation failed",
        ],
        [
            "0787133b-cb55-4a31-9480-1e04b7b72898",
            {"title": "me", "author": "me@testdriven.io"},
            404,
            "Book 0787133b-cb55-4a31-9480-1e04b7b72898 does not exist",
        ],
    ],
)
def test_update_book_invalid(test_app, monkeypatch, book_id, payload, status_code, message):
    def mock_get_book_by_id(book_id):
        return None
    monkeypatch.setattr(src.api.books, "get_book_by_id", mock_get_book_by_id)
    client = test_app.test_client()
    resp = client.put(
        f"/books/{book_id}", data=json.dumps(payload), content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]


def test_update_book_duplicate_author(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self
    def mock_get_book_by_id(book_id):
        d = AttrDict()
        d.update({
            "id": "0787133b-cb55-4a31-9480-1e04b7b72898",
            "title": "me",
            "author": "me@testdriven.io"
        })
        return d
    def mock_update_book(book, title, author):
        return True
    def mock_get_book_by_title(author):
        return True
    monkeypatch.setattr(src.api.books, "get_book_by_id", mock_get_book_by_id)
    monkeypatch.setattr(src.api.books, "get_book_by_title", mock_get_book_by_title)
    monkeypatch.setattr(src.api.books, "update_book", mock_update_book)
    client = test_app.test_client()
    resp = client.put(
        "/books/0787133b-cb55-4a31-9480-1e04b7b72898",
        data=json.dumps({"title": "me", "author": "me@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That book already exists." in data["message"]