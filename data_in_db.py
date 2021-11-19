import pandas as pd
from datetime import date, datetime

from book_rental.create import db, create_app
from book_rental.src.model import Book

app = create_app()
with app.app_context():
    data = pd.read_excel("./library.xlsx")

    for i in range(len(data)):
        row = data.iloc[i]
        published_at = datetime.strptime(str(row['publication_date'])[:10], '%Y-%m-%d').date()
        image_path = f"/static/image/{row['id']}"
        try:
            open(f'book_rental/{image_path}.png')
            image_path += '.png'
        except:
            image_path += '.jpg'
        book = Book(
            book_name=row['book_name'], 
            book_publisher=row['publisher'],
            book_author=row['author'], 
            book_publication_date=published_at, 
            book_pages=int(row['pages']),
            book_isbn=row['isbn'], 
            book_description=row['description'], 
            book_link=image_path,
        )
        db.session.add(book)
        print("in_data")
        

    db.session.commit()