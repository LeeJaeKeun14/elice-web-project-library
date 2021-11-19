# application/src/views/__init__.py
from flask import Blueprint
from book_rental.create import db
from book_rental.src.model import *

api_auth = Blueprint("auth", __name__, url_prefix='/auth')

from .auth import *