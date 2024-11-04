from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db
import json
from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
# from ..models.book import books

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()

    return create_model(Book, request_body)

@bp.get("")
def get_all_books():
    
    return get_models_with_filters(Book, request.args)

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    
    return book.to_dict()

@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    response = f"Book #{book_id} successfully updated"
    # return Response(response, status=200, mimetype="application/json")
    return Response(json.dumps(response),status=200, mimetype="application/json")

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    response = f"Book #{book_id} successfully deleted"
    return Response(json.dumps(response),status=200, mimetype="application/json")