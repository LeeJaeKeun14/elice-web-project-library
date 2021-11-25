from book_rental.create import db
from datetime import datetime
from datetime import timedelta

# 유저 정보
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(30), nullable=False, unique=True)
    user_pw = db.Column(db.Text(), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_nickname = db.Column(db.String(100), nullable=False, unique=True)
    
    # 책 대여 외부키
    bookrental = db.relationship("Book_rental", backref="user")
    # 책_평가 외부키
    bookevaluation = db.relationship("Book_evaluation", backref="user")
    
    def __init__(self,user_id,user_pw,user_name,user_nickname):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_name = user_name
        self.user_nickname = user_nickname

# 책 정보
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(100), nullable=False)
    book_publisher = db.Column(db.String(100), nullable=False)
    book_author = db.Column(db.String(100), nullable=False)
    book_publication_date = db.Column(db.DateTime, nullable=False)
    book_pages = db.Column(db.Integer, nullable=False)
    book_isbn = db.Column(db.BigInteger, nullable=False)
    book_description = db.Column(db.Text(), nullable=False)
    book_link = db.Column(db.String(60), nullable=False)
    
    # 책 보유 외부키
    bookstock = db.relationship("Book_stock", backref="book")
    # 책_평가 외부키
    bookevaluation = db.relationship("Book_evaluation", backref="book")
    
    def __init__(self,book_name,book_publisher,book_author,book_publication_date,
                book_pages,book_isbn,book_description,book_link):
        self.book_name = book_name
        self.book_publisher = book_publisher
        self.book_author = book_author
        self.book_publication_date = book_publication_date
        self.book_pages = book_pages
        self.book_isbn = book_isbn
        self.book_description = book_description
        self.book_link=book_link

# 책 보유 정보
class Book_stock(db.Model):
    __tablename__ = 'book_stock'
    book_serial_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable = False)
    is_rental = db.Column(db.Boolean, nullable = False)

    # 대여_책 외부키
    bookrental = db.relationship("Book_rental", backref="book_stock")
    
    def __init__(self,book_id,is_rental):
        self.book_id = book_id
        self.is_rental = is_rental

# 책 대여 정보
class Book_rental(db.Model):
    __tablename__ = 'book_rental'
    id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), 
                            nullable = False)
    book_serial_number = db.Column(db.Integer, db.ForeignKey("book_stock.book_serial_number"), 
                            nullable = False)
    rental_date = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(hours=9))
    return_date = db.Column(db.DateTime)
    is_return = db.Column(db.Boolean, nullable = False)
    
    def __init__(self,user_id,book_serial_number,return_date,is_return):
        self.user_id = user_id
        self.book_serial_number = book_serial_number
        self.return_date = return_date
        self.is_return = is_return

# 책 평가 정보
class Book_evaluation(db.Model):
    __tablename__ = 'book_evaluation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    book_evaluation = db.Column(db.Integer, nullable = False)
    evaluation_contente = db.Column(db.Text(), nullable = False)
    evaluation_time = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(hours=9))
    evaluation_delete = db.Column(db.Boolean, default=True)
    evaluation_contente
    def __init__(self,book_id,user_id,book_evaluation,evaluation_contente):
        self.book_id = book_id
        self.user_id = user_id
        self.book_evaluation = book_evaluation
        self.evaluation_contente = evaluation_contente