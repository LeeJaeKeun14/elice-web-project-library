from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
from . import api_book

@api_book.before_app_request
def load_logged_in_user():
    id = session.get('user_id')
    if id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == id).first()

@api_book.route('/rental/<book_id>', methods=('GET', 'POST'))
def rental(book_id):
    
    return redirect(url_for('book.detail', book_id=book_id))

@api_book.route('/detail/<book_id>', methods=('GET', 'POST'))
def detail(book_id):
    
    book_detail = db.session.query(Book).filter(Book.id == book_id).first()
            
    data = {
        "book_detail":book_detail
    }
    return render_template("detail.html", data=data)