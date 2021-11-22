from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
from . import api_index

@api_index.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.user_id == user_id).first()

@api_index.route("/")
def index():
    
    new_book = db.session.query(Book).order_by(Book.book_publication_date.desc()).all()
    new_book = new_book[:5]
    
    # eval_book = db.session.query(Book, Book_evaluation).\
    #                 filter(Book.id==Book_evaluation.book_id).\
    #                 all()
    # for a, b in eval_book:
    #     print(a, b)

    data = {
        "new_book":new_book
    }
    return render_template('index.html', data=data)
