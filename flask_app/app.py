from flask import Flask, render_template
import json
import os
from pathlib import Path


DIR_PATH = os.getcwd()
file_path = Path(str(Path(DIR_PATH).parent) + "\Applications_info.json")

with open(file_path, 'r') as f:
    admin_info = json.load(f)

sql_key = admin_info["mysql"]["pw"]

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{sql_key}@127.0.0.1:3307/elice_book_rental"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app