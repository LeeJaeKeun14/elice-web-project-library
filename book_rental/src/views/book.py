from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
from math import ceil
import pandas as pd
import json
from datetime import datetime
from . import api_book

@api_book.before_app_request
def load_logged_in_user():
    id = session.get('user_id')
    if id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == id).first()

# 책 대여 페이지
@api_book.route('/rental/<book_id>', methods=('GET', 'POST'))
def rental(book_id):

    if session.get('user_id') is None: # 로그인 여부 확인
        return redirect(url_for('auth.book_signin', book_id=book_id, method="rental"))
    # 대여기능
    if request.method == 'POST':
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
@api_book.route('/detail/<book_id>')
def detail(book_id):
    
    evaluation_book = db.session.query(Book_evaluation).\
                                filter(Book_evaluation.book_id == book_id).all()
    # queryset = Book_stock.query.filter(Book_stock.book_serial_number > 0)
    # df_stock = pd.read_sql(queryset.statement, queryset.session.bind) 
    # df_stock = df_stock[["book_serial_number", "book_id"]]
    # df = df.merge(df_stock, "left", on="book_serial_number")
    
    # queryset = Book.query.filter(Book.id > 0) 
    # df_book = pd.read_sql(queryset.statement, queryset.session.bind)  

    # queryset = Book_evaluation.query.filter(Book_evaluation.id > 0)  
    # df_eval = pd.read_sql(queryset.statement, queryset.session.bind)
    
    # # 책 평가 평균값 구하기
    # df_eval = df_eval[["book_id", "book_evaluation"]]
    # df_eval["book_evaluation"] = df_eval["book_evaluation"].astype("int")
    # df_eval = df_eval[["book_id", "book_evaluation"]].groupby("book_id").mean()
    
    # # 책 정보에 평가를 합치고, 값이 없을경우 0점 부여
    # df_book = df_book.merge(df_eval, "left", left_on="id", right_on="book_id")
    # df_book['book_evaluation'] = df_book['book_evaluation'].fillna(0)
    # df_book['book_evaluation'] = df_book['book_evaluation'].astype("int")
    # # 책 내용 책 평가 책 대여 기록
    
    # df = df.merge(df_book, "left", left_on="book_id" ,right_on="id")
    # df.rental_date = df.rental_date.astype("str")
    
    # offset = (page - 1) * limit
    # return_books = df[offset:offset+limit]
    # return_books = json.loads(return_books.to_json(orient="records"))
    
    
    
    
    detail_book = db.session.query(Book).filter(Book.id == book_id).first()
    
    data = {
        "detail_book":detail_book,
        "evaluation_book":evaluation_book
    }
    return render_template("detail.html", data=data)

@api_book.route('/detail/<book_id>/contente', methods=('GET', 'POST'))
def contente(book_id):
    # 댓글 기능
    user_id = g.user.user_id
    
    return redirect(url_for('book.detail', book_id=book_id))


    
@api_book.route('/return_book/<page>', methods=('GET', 'POST'))
def return_book(page):
    
    # 세션 확인 로그인 만 가능
    if session.get('user_id') is None: # 로그인 여부 확인
        return redirect(url_for('index.index'))
    
    if request.method == 'POST':
        book_serial_number = request.form.get('book_serial_number', None)

        rental_book = db.session.query(Book_rental).\
                                filter(Book_rental.book_serial_number == book_serial_number).\
                                filter(Book_rental.user_id == g.user.id).\
                                filter(Book_rental.is_return == 0).first()
        rental_book.is_return = 1
        rental_book.return_date = datetime.utcnow()
        
        db.session.add(rental_book)
        
        # 해당 일련번호
        # 북 스톡에서 is_rental 0 으로 수정
        stock_book = db.session.query(Book_stock).\
                                filter(Book_stock.book_serial_number == book_serial_number).first()
        stock_book.is_rental = 0
        db.session.add(stock_book)
        db.session.commit()
        
        return redirect(url_for('index.index'))
    
    page = int(page)
    return_books_count = db.session.query(Book_rental).\
                            filter(Book_rental.user_id == g.user.id).\
                            filter(Book_rental.is_return == 0).count()
    # db 접근
    
    limit = 8
    totalPage = ceil(return_books_count / 8)
    if totalPage == 0:
        page = 1
        totalPage = 1
    elif page >= totalPage:
        page = totalPage
    
    
    # book_rental 기준
    queryset = Book_rental.query.\
                        filter(Book_rental.user_id == g.user.id).\
                        filter(Book_rental.is_return == 0)
    df = pd.read_sql(queryset.statement, queryset.session.bind) 
    
    # book_stock
    queryset = Book_stock.query.filter(Book_stock.book_serial_number > 0)
    df_stock = pd.read_sql(queryset.statement, queryset.session.bind) 
    df_stock = df_stock[["book_serial_number", "book_id"]]
    df = df.merge(df_stock, "left", on="book_serial_number")
    
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
    df.rental_date = df.rental_date.astype("str")
    
    offset = (page - 1) * limit
    return_books = df[offset:offset+limit]
    return_books = json.loads(return_books.to_json(orient="records"))
    
    # 현재 페이지도 보내야함 "page":page
    # 전체 페이지도 배냐야함
    # 대여 기준일 정렬
    data = {
        "return_books": return_books,
        "page": page,
        "totalPage": totalPage
    }
    return render_template("return_book.html", data=data)

@api_book.route('/rental_list/<page>')
def rental_list(page):
    
    if session.get('user_id') is None: # 로그인 여부 확인
        return redirect(url_for('index.index'))
    
    # 세션 확인 로그인 만 가능
    page = int(page)
    rental_books_count = db.session.query(Book_rental).\
                            filter(Book_rental.user_id == g.user.id).\
                            filter(Book_rental.is_return == 1).count()
    # db 접근
    
    limit = 8
    totalPage = ceil(rental_books_count / 8)
    if totalPage == 0:
        page = 1
        totalPage = 1
    elif page >= totalPage:
        page = totalPage
    
    
    # book_rental 기준
    queryset = Book_rental.query.\
                        filter(Book_rental.user_id == g.user.id).\
                        filter(Book_rental.is_return == 1)
    df = pd.read_sql(queryset.statement, queryset.session.bind) 
    
    # book_stock
    queryset = Book_stock.query.filter(Book_stock.book_serial_number > 0)
    df_stock = pd.read_sql(queryset.statement, queryset.session.bind) 
    df_stock = df_stock[["book_serial_number", "book_id"]]
    df = df.merge(df_stock, "left", on="book_serial_number")
    
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
    df.rental_date = df.rental_date.astype("str")
    df.return_date = df.return_date.astype("str")
    
    offset = (page - 1) * limit
    rental_books = df[offset:offset+limit]
    rental_books = json.loads(rental_books.to_json(orient="records"))
    
    # 현재 페이지도 보내야함 "page":page
    # 전체 페이지도 배냐야함
    # 대여 기준일 정렬
    data = {
        "rental_books": rental_books,
        "page": page,
        "totalPage": totalPage
    }
    return render_template("rental_list.html", data=data)