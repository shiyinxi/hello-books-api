from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db
import json
from app.routes.route_utilities import validate_model
# from ..models.book import books

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()

    try: 
        new_book = Book.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

@bp.get("")
def get_all_books():
    title_param = request.args.get("title")
    if title_param:
        query = db.select(Book).where(Book.title.ilike(f"%{title_param}%")).order_by(Book.id)
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))
    
    query = query.order_by(Book.id)
   
    books = db.session.scalars(query)

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
         
    return books_response

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