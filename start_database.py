from book_rental.create import db, create_app
from book_rental.src.model import User, Book_rental, Book_evaluation
from flask_bcrypt import Bcrypt
from datetime import datetime
from datetime import timedelta

bcrypt = Bcrypt()

app = create_app()
with app.app_context():

    pw = "1a2w3e4r%T"
    pw_hash = bcrypt.generate_password_hash(pw)
    

    user = User("ljkean@gmail.com", pw_hash,"이재근", "관리자")
    db.session.add(user)
    rental_book = Book_rental(1, 1, datetime.utcnow() + timedelta(hours=9),1)
    db.session.add(rental_book)
    evaluation_book = Book_evaluation(1, 1, 5, "좋아")
    db.session.add(evaluation_book)
        
    db.session.commit()