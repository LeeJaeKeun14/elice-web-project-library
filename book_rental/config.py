# application/config.py
# 모든 config 설정들을 여기서 관리합니다.
# current_app.config 를 통해서도 접근이 가능합니다.
import json
import os
from pathlib import Path

DIR_PATH = os.getcwd()
file_path = Path(str(Path(DIR_PATH).parent) + "\Applications_info.json")

with open(file_path, 'r') as f:
    admin_info = json.load(f)
sql_id = admin_info["mysql"]["id"]
sql_pw = admin_info["mysql"]["pw"]

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI  = f"mysql+pymysql://{sql_id}:{sql_pw}@127.0.0.1:3307/elice_book_rental"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MESSAGE = 'Product'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI  = f"mysql+pymysql://{sql_id}:{sql_pw}@127.0.0.1:3307/elice_book_rental"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    MESSAGE = 'Development'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI  = f"mysql+pymysql://{sql_id}:{sql_pw}@127.0.0.1:3307/elice_book_rental"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    MESSAGE = 'Testing'

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)