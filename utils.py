import requests
from flask import current_app
from extensions import db
from models import Book

def fetch_book_by_isbn(isbn):
    key = current_app.config['GOOGLE_BOOKS_API_KEY']
    resp = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': 'isbn:' + isbn, 'key': key})
    resp.raise_for_status()
    items = resp.json().get('items')
    if not items: return None
    info = items[0]['volumeInfo']
    book = Book.query.filter_by(isbn=isbn).first()
    if not book:
        book = Book(isbn=isbn,
                    title=info.get('title'),
                    authors=', '.join(info.get('authors', [])),
                    pages=info.get('pageCount'),
                    cover=info.get('imageLinks', {}).get('thumbnail'))
        db.session.add(book); db.session.commit()
    return book
