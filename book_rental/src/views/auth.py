from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template, g
from flask_bcrypt import Bcrypt
from book_rental.src.model import User, Book, Book_stock, Book_rental, Book_evaluation
from book_rental.create import db
from . import api_auth

# api_auth = Blueprint("auth", __name__)

@api_auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.user_id == user_id).first()

@api_auth.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        user_id = request.form.get('user_id', None)
        user_pw = request.form.get('user_pw', None)
        user_name = request.form.get('user_name', None)
        user_nickname = request.form.get('user_nickname', None)
        
        message, messageType = None, None
        
        ## 아이디 중복 검사 아이디어 고민중...
        if user_id is None:
            message, messageType = '아이디가 유효하지 않습니다.', 'danger'
        elif user_pw is None:
            message, messageType = '비밀번호가 유효하지 않습니다.', 'danger'
        else:
            user = db.session.query(User).filter(User.user_id == user_id).first()
            if user is not None:
                message, messageType = f'{user_id} 계정은 이미 등록된 계정입니다.', 'warning'
            
        if message is None:
            # 유저 테이블에 추가

            pw_hash = Bcrypt.generate_password_hash(user_pw)
            
            user = User(user_id, pw_hash, user_name, user_nickname)
            db.session.add(user)
            db.session.commit()
            
            return redirect(url_for('auth.signin'))
        
        flash(message=message, category=messageType)

    return render_template('signup.html')


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

    return redirect(url_for('index.index'))



@api_auth.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index.index'))