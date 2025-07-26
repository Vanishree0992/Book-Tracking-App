from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from models import User, Book, Review
from forms import LoginForm, RegisterForm, AddBookForm, ReviewForm, ChallengeForm
from extensions import db, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from utils import fetch_book_by_isbn
from flask import send_file
import json, os
from io import BytesIO
from reportlab.pdfgen import canvas

app = Flask(__name__)
@login_manager.user_loader
def load_user(uid): return User.query.get(int(uid))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.check_password(form.password.data):
            login_user(u); return redirect(url_for('profile'))
        flash('Invalid credentials.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u); db.session.commit()
        flash('Registered. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user(); return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    shelf = json.loads(current_user.bookshelf or '[]')
    books = Book.query.filter(Book.isbn.in_(shelf)).all()
    return render_template('profile.html', books=books)

@app.route('/add-book', methods=['GET','POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        b = fetch_book_by_isbn(form.isbn.data.strip())
        if b:
            shelf = json.loads(current_user.bookshelf or '[]')
            if b.isbn not in shelf:
                shelf.append(b.isbn)
                current_user.bookshelf = json.dumps(shelf); db.session.commit()
            return redirect(url_for('profile'))
        flash('Book not found.')
    return render_template('add_book.html', form=form)

@app.route('/book/<isbn>', methods=['GET','POST'])
@login_required
def book_detail(isbn):
    b = Book.query.filter_by(isbn=isbn).first_or_404()
    form = ReviewForm()
    if form.validate_on_submit():
        r = Review(rating=form.rating.data, comment=form.comment.data, book=b, user=current_user)
        db.session.add(r); db.session.commit()
        flash('Review added.')
        return redirect(url_for('book_detail', isbn=isbn))
    reviews = Review.query.filter_by(book=b).all()
    return render_template('book_detail.html', book=b, form=form, reviews=reviews)

@app.route('/wishlist')
@login_required
def wishlist():
    wl = json.loads(current_user.wishlist or '[]')
    books = Book.query.filter(Book.isbn.in_(wl)).all()
    return render_template('wishlist.html', books=books)

@app.route('/set_challenge', methods=['GET','POST'])
@login_required
def challenge():
    form = ChallengeForm()
    if form.validate_on_submit():
        current_user.challenges = json.dumps({'target': form.target.data, 'completed': 0})
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('challenge.html', form=form, challenge=json.loads(current_user.challenges or '{}'))

@app.route('/export')
@login_required
def export_library():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    shelf = json.loads(current_user.bookshelf or '[]')
    y = 800
    p.drawString(100, y, f"{current_user.username}'s Library:")
    for isbn in shelf:
        y -= 20
        p.drawString(100, y, isbn)
    p.showPage(); p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='library.pdf', mimetype='application/pdf')
