from book_rental.create import db, create_app
from book_rental.src.model import Book, Book_stock

app = create_app()
num = 3
with app.app_context():

    book = db.session.query(Book).all()
    for b in book:
        print(b.id)
        for _ in range(num):
            book_stock = Book_stock(
                book_id=int(b.id),
                is_rental=False
            )
            db.session.add(book_stock)
        print("in_data")
        
    db.session.commit()