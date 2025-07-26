from extensions import db
from flask_login import UserMixin
from datetime import datetime
import json

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(200))
    bookshelf = db.Column(db.Text, default='[]')      # list of book ISBNs
    wishlist = db.Column(db.Text, default='[]')
    challenges = db.Column(db.Text, default='[]')     # JSON reading challenge

    def set_password(self, pw): from werkzeug.security import generate_password_hash; self.password_hash = generate_password_hash(pw)
    def check_password(self, pw): from werkzeug.security import check_password_hash; return check_password_hash(self.password_hash, pw)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200))
    authors = db.Column(db.String(200))
    pages = db.Column(db.Integer)
    cover = db.Column(db.String(200))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book = db.relationship('Book', backref='reviews')
    user = db.relationship('User', backref='reviews')
