import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///books.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY', 'YOUR_KEY')
    GOODREADS_API_KEY = os.environ.get('GOODREADS_API_KEY', 'YOUR_KEY')
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
