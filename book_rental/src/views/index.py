from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
import json
from . import api_index

import pandas as pd

@api_index.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.user_id == user_id).first()

@api_index.route("/")
def index():

    # 책 DataFrame
    queryset = Book.query.filter(Book.id > 0) 
    df = pd.read_sql(queryset.statement, queryset.session.bind)  

    # 책 평가 DataFrame
    queryset = Book_evaluation.query.filter(Book_evaluation.id > 0)  
    df_eval = pd.read_sql(queryset.statement, queryset.session.bind)
    
    # 책 평가 평균값 구하기
    df_eval = df_eval[["book_id", "book_evaluation"]]
    df_eval["book_evaluation"] = df_eval["book_evaluation"].astype("int")
    df_eval = df_eval[["book_id", "book_evaluation"]].groupby("book_id").mean()
    
    # 책 정보에 평가를 합치고, 값이 없을경우 0점 부여
    df = df.merge(df_eval, "left", left_on="id", right_on="book_id")
    df['book_evaluation'] = df['book_evaluation'].fillna(0)
    df['book_evaluation'] = df['book_evaluation'].astype("int")

    new_book = df.sort_values("book_publication_date", ascending=False)[:5]
    eval_book = df.sort_values("book_evaluation", ascending=False)[:5]
    
    rent_book_count = 0
    if session.get('user_id') is not None: # 로그인 여부 확인
        rent_book_count = db.session.query(Book_rental).\
                        filter(Book_rental.user_id == g.user.id).\
                        filter(Book_rental.is_return == 0).count()
    
    new_book = json.loads(new_book.to_json(orient="records"))
    eval_book = json.loads(eval_book.to_json(orient="records"))
    
    data = {
        "new_book": new_book,
        "eval_book": eval_book,
        "rent_book_count": rent_book_count
    }
    return render_template('index.html', data=data)
