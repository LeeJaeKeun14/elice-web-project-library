from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
import re
from . import api_auth

# api_auth = Blueprint("auth", __name__)

@api_auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.user_id == user_id).first()

# 중복확인 버튼 고민 흔적
# @api_auth.route('/duplicate_id', methods=('GET', 'POST'))
# def duplicate_id():
#     print("중복확인")
#     flash(message={"중복확인"}, category="danger")
#     return jsonify({"result":"중복확인"})

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
            pw_e = re.compile("[a-zA-Z]+")
            pw_n = re.compile("[0-9]+")
            pw_s = re.compile("[^a-zA-Z0-9 \t\n\r\f\v]+")
            name = re.compile("[가-힣a-zA-Z]")
            
            ## 아이디 이메일 검사
            if email.match(user_id) == None:
                message, messageType = '아이디를 이메일 형식으로 만들어야 합니다.', 'danger'
            elif len(user_id) > 30:
                message, messageType = '아이디를 30자 이내로 만들어야 합니다.', 'danger'
            ## 아이디 중복 검사
            elif db.session.query(User).filter(User.user_id == user_id).first() is not None:
                message, messageType = f'{user_id} 계정은 이미 등록된 계정입니다.', 'warning'
            ## 비밀번호 10자 이상 영문, 숫자, 특수문자 중 2개 사용
            elif len(user_pw) >= 10 and \
            ((pw_e.match(user_pw) and pw_n.match(user_pw)) or \
            (pw_e.match(user_pw) and pw_s.match(user_pw)) or \
            (pw_n.match(user_pw) and pw_s.match(user_pw))):
                message, messageType = '비밀번호가 유효하지 않습니다.', 'danger'
            ## 비밀번호 8자 이상 영문, 숫자, 특수문자 모두 사용
            elif len(user_pw) >= 10 and pw_e.match(user_pw) and pw_n.match(user_pw) and pw_s.match(user_pw):
                message, messageType = '비밀번호가 유효하지 않습니다.', 'danger'
            ## 비밀번호 확인과 비밀번호 같은지 확인
            elif user_pw != user_pw_check:
                message, messageType = '비밀번호가 비밀번호확인과 동일하지 않습니다.', 'danger'
            ## 이름은 한글과 영문으로만 입력 받아야 합니다.
            elif user_pw is None:
                # 정규표현식
                message, messageType = '비밀번호가 유효하지 않습니다.', 'danger'
            ## 닉네임 중복 확인
            elif db.session.query(User).filter(User.user_nickname == user_nickname).first() is not None:
                message, messageType = f'{user_nickname} 닉네임은 이미 등록된 닉네임입니다.', 'warning'
            
            if message is None:
                # 유저 테이블에 추가
                # 비밀번호 암호화
                pw_hash = Bcrypt.generate_password_hash(user_pw)
                
                user = User(user_id, pw_hash, user_name, user_nickname)
                db.session.add(user)
                db.session.commit()
                
                return redirect(url_for('auth.signin'))
            
            flash(message=message, category=messageType)

        return render_template('signup.html')
    # 로그인 시 메인화면으로 이동
    return redirect(url_for('index.index'))


@api_auth.route('/signin', methods=('GET', 'POST'))
def signin():
    if session.get('user_id') is None:
        if request.method == 'POST':
            user_id = request.form.get('user_id', None)
            user_pw = request.form.get('user_pw', None)
            
            user = User.query.filter(User.user_id == user_id).first()
            message, messageType = None, None

            if user is None:
                message, messageType = '등록되지 않은 계정입니다.', 'danger'
            elif not Bcrypt.check_password_hash(user.user_pw, user_pw):
                message, messageType = '비밀번호가 틀렸습니다.', 'danger'

            if message is None:
                session.clear()
                session['user_id'] = user['user_id']
                return redirect(url_for('index.index'))

            flash(message=message, category=messageType)
        return render_template('signin.html')
    # 로그인 시 메인화면으로 이동
    return redirect(url_for('index.index'))



@api_auth.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index.index'))