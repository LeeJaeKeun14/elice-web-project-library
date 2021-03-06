# application/src/views/__init__.py
from flask import Blueprint
from book_rental.create import db
from book_rental.src.model import *

api_auth = Blueprint("auth", __name__, url_prefix='/auth')
from .auth import *

api_index = Blueprint("index", __name__)
from .index import *

api_book = Blueprint("book", __name__, url_prefix='/book')
from .book import *