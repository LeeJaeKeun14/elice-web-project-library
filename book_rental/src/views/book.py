from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
from math import ceil
import pandas as pd
import json
from . import api_book

@api_book.before_app_request
def load_logged_in_user():
    id = session.get('user_id')
    if id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == id).first()

# 책 빌리기
@api_book.route('/rent/<book_id>', methods=('GET', 'POST'))
def rent(book_id):
    message, messageType = None, None
    
    stock_book = db.session.query(Book_stock).\
                        filter(Book_stock.book_id == book_id).\
                        filter(Book_stock.is_rental == 0).first()
    # 없을경우 대여할 수 없습니다.
    if stock_book == None:
        message, messageType = '대여할 수 있는 책이 없습니다.', 'danger'

    book_stock = db.session.query(Book_stock).\
                        filter(Book_stock.book_id == book_id).first()
    rent_user = db.session.query(Book_rental).\
                        filter(Book_rental.book_serial_number == book_stock.book_serial_number).\
                        filter(Book_rental.user_id == g.user.id).\
                        filter(Book_rental.is_return == 0).first()
    # 이미 대여중일 경우 대여할 수 없습니다.
    if rent_user != None:
        message, messageType = '책을 이미 대여중입니다.', 'danger'
        
    if message is None:
        stock_book.is_rental = 1
        db.session.add(stock_book)
        
        rent_book = Book_rental(g.user.id, stock_book.book_serial_number, None, 0)
        db.session.add(rent_book)
        db.session.commit()
        return redirect(url_for('index.index'))
    
    flash(message=message, category=messageType)
    return redirect(url_for('book.rental', book_id=book_id))

# 책 빌리는 페이지
@api_book.route('/rental/<book_id>', methods=('GET', 'POST'))
def rental(book_id):
    if session.get('user_id') is None: # 로그인 여부 확인
        return redirect(url_for('auth.book_signin', book_id=book_id, method="rental"))
    # 대여기능
    
    stock_book_count = db.session.query(Book_stock).\
                            filter(Book_stock.book_id == book_id).\
                            filter(Book_stock.is_rental == 0).count()
    detail_book = db.session.query(Book).filter(Book.id == book_id).first()
    # 보관중인 책 가져와 정보 반환
    data = {
        "detail_book": detail_book,
        "stock_book_count":stock_book_count
    }
    return render_template("rental_book.html", data=data)

# 책 상세페이지
@api_book.route('/detail/<book_id>', methods=('GET', 'POST'))
def detail(book_id):
    
    detail_book = db.session.query(Book).filter(Book.id == book_id).first()
            
    data = {
        "detail_book":detail_book
    }
    return render_template("detail.html", data=data)

@api_book.route('/detail/<book_id>/contente', methods=('GET', 'POST'))
def contente(book_id):
    # 댓글 기능
    user_id = g.user.user_id
    
    return redirect(url_for('book.detail', book_id=book_id))
    
    
    
@api_book.route('/return_book', methods=('GET', 'POST'))
def return_book():
    # 세션 확인 로그인 만 가능
    
    q = request.args.get('q', None)
    page = int(request.args.get('page', 1))
    
    user_id = g.user.user_id
    
    data = {
        
    }
    return render_template("return_book.html", data=data)

@api_book.route('/return_book_list', methods=('GET', 'POST'))
def return_book_list():
    
    page = int(request.args.get('page', 1))
    
    return_books_count = db.session.query(Book_rental).\
                            filter(Book_rental.user_id == g.user.id).\
                            filter(Book_rental.is_return == 0).count()
    # db 접근
    
    limit = 8
    totalPage = ceil(return_books_count / 10)
    if totalPage == 0:
        page = 1
        totalPage = 1
    elif page >= totalPage:
        page = totalPage
    
    # book_rental 기준
    queryset = Book_rental.query.filter(Book_rental.id > 0) 
    df = pd.read_sql(queryset.statement, queryset.session.bind) 
    
    queryset = Book.query.filter(Book.id > 0) 
    df_book = pd.read_sql(queryset.statement, queryset.session.bind)  

    queryset = Book_evaluation.query.filter(Book_evaluation.id > 0)  
    df_eval = pd.read_sql(queryset.statement, queryset.session.bind)
    
    # 책 평가 평균값 구하기
    df_eval = df_eval[["book_id", "book_evaluation"]]
    df_eval["book_evaluation"] = df_eval["book_evaluation"].astype("int")
    df_eval = df_eval[["book_id", "book_evaluation"]].groupby("book_id").mean()
    
    # 책 정보에 평가를 합치고, 값이 없을경우 0점 부여
    df_book = df_book.merge(df_eval, "left", left_on="id", right_on="book_id")
    df_book['book_evaluation'] = df_book['book_evaluation'].fillna(0)
    df_book['book_evaluation'] = df_book['book_evaluation'].astype("int")
    # 책 내용 책 평가 책 대여 기록
    
    df = df.merge(df_book, "left", left_on="book_id" ,right_on="id")
    
    offset = (page - 1) * limit
    result = df[offset:offset+limit]
        
    result = json.loads(result.to_json(orient="records"))
    
    return jsonify(result=result, totalPage=totalPage)