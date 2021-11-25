from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
import re
from . import api_auth

bcrypt = Bcrypt()

@api_auth.before_app_request
def load_logged_in_user():
    id = session.get('user_id')
    if id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == id).first()

# 회원가입
@api_auth.route('/signup', methods=('GET', 'POST'))
def signup():
    if session.get('user_id') is None: # 로그인 여부 확인
        if request.method == 'POST':
            user_id = request.form.get('user_id', None)
            user_pw = request.form.get('user_pw', None)
            user_pw_check = request.form.get('user_pw_check', None)
            user_name = request.form.get('user_name', None)
            user_nickname = request.form.get('user_nickname', None)
            
            message, messageType = None, None
            
            # 정규표현식
            email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            pw_check_1 = re.compile("^(?=.*[a-zA-Z])(?=.*\d)[^ \t\n\r\f\v]")
            pw_check_2 = re.compile("^(?=.*\d)(?=.*[-=+,#/\?:^$.@*\"~&%ㆍ!\\‘|\(\)\[\]\<\>`\'])[^ \t\n\r\f\v]")
            pw_check_3 = re.compile("^(?=.*[a-zA-Z])(?=.*[-=+,#/\?:^$.@*\"~&%ㆍ!\\‘|\(\)\[\]\<\>`\'])[^ \t\n\r\f\v]")
            password = re.compile("^(?=.*[a-zA-Z])(?=.*\d)(?=.*[-=+,#/\?:^$.@*\"~&%ㆍ!\\‘|\(\)\[\]\<\>`\'])[^ \t\n\r\f\v]")
            name = re.compile("[가-힣a-zA-Z]")
            ## 아이디 이메일 검사
            if email.match(user_id) == None:
                message, messageType = '아이디를 이메일 형식으로 만들어야 합니다.', 'danger'
            elif len(user_id) > 30:
                message, messageType = '아이디를 30자 이내로 만들어야 합니다.', 'danger'
            ## 아이디 중복 검사
            elif db.session.query(User).filter(User.user_id == user_id).first() is not None:
                message, messageType = f'{user_id} 계정은 이미 등록된 계정입니다.', 'warning'
            ## 비밀번호 검증
            elif len(user_pw) < 8:
                message, messageType = '비밀번호를 8자 이상, 영문, 숫자, 특수문자를 포함되게 만들어야 합니다.', 'danger'
            elif 8 <= len(user_pw) < 10 and password.match(user_pw) == None:
                message, messageType = '비밀번호를 영문, 숫자, 특수문자를 포함되게 만들어야 합니다.', 'danger'
            ## 영문 숫자, 영문 특수문자, 숫자 특수문자를 하나라도 만족하지 않을경우 
            elif pw_check_1.match(user_pw) == None and pw_check_2.match(user_pw) == None and pw_check_3.match(user_pw) == None:
                message, messageType = '비밀번호가 영문, 숫자, 특수문자 중 2개이상을 포함되게 만들어야 합니다.', 'danger'
            ## 비밀번호 확인과 비밀번호 같은지 확인
            elif user_pw != user_pw_check:
                message, messageType = '비밀번호와 비밀번호확인이 동일하지 않습니다.', 'danger'
            ## 이름은 한글과 영문으로만 입력 받아야 합니다.
            elif name.match(user_name) == None:
                message, messageType = '이름을 영문, 한글로만 작성해야 합니다.', 'danger'
            ## 닉네임 중복 확인
            elif db.session.query(User).filter(User.user_nickname == user_nickname).first() is not None:
                message, messageType = f'{user_nickname} 닉네임은 이미 등록된 닉네임입니다.', 'warning'
            
            if message is None:
                # 유저 테이블에 추가
                # 비밀번호 암호화
                pw_hash = bcrypt.generate_password_hash(user_pw)
                
                user = User(user_id, pw_hash, user_name, user_nickname)
                db.session.add(user)
                db.session.commit()
                
                return redirect(url_for('auth.signin'))
            
            flash(message=message, category=messageType)

        return render_template('signup.html')
    # 로그인 시 메인화면으로 이동
    return redirect(url_for('index.index'))

# 로그인
@api_auth.route('/signin', methods=('GET', 'POST'))
def signin():
    if session.get('user_id') is None:
        if request.method == 'POST':
            user_id = request.form.get('user_id', None)
            user_pw = request.form.get('user_pw', None)
            
            user = db.session.query(User).filter(User.user_id == user_id).first()
            message, messageType = None, None

            if user is None:
                message, messageType = '등록되지 않은 계정입니다.', 'danger'
            elif not bcrypt.check_password_hash(user.user_pw, user_pw):
                message, messageType = '비밀번호가 틀렸습니다.', 'danger'

            if message is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('index.index'))

            flash(message=message, category=messageType)
        return render_template('signin.html', method="")
    # 로그인 시 메인화면으로 이동
    return redirect(url_for('index.index'))

@api_auth.route('/book_signin/<book_id>/<method>', methods=('GET', 'POST'))
def book_signin(book_id, method):
    if session.get('user_id') is None:
        if request.method == 'POST':
            user_id = request.form.get('user_id', None)
            user_pw = request.form.get('user_pw', None)
            
            user = db.session.query(User).filter(User.user_id == user_id).first()
            message, messageType = None, None

            if user is None:
                message, messageType = '등록되지 않은 계정입니다.', 'danger'
            elif not bcrypt.check_password_hash(user.user_pw, user_pw):
                message, messageType = '비밀번호가 틀렸습니다.', 'danger'

            if message is None:
                session.clear()
                session['user_id'] = user.id
                # method를 확인하여 해당 링크로 이동
                if method == "rental":
                    return redirect(url_for('book.rental', book_id=book_id))
                return redirect(url_for('book.detail', book_id=book_id))

            flash(message=message, category=messageType)
        return render_template('signin.html', method=method)
    # method를 확인하여 해당 링크로 이동
    if method == "rental":
        return redirect(url_for('book.rental', book_id=book_id))
    return redirect(url_for('book.detail', book_id=book_id))


@api_auth.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index.index'))