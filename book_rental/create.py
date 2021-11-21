from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config='dev'):
    app = Flask(__name__)
    
    # config 속성 부여
    from .config import config_by_name
    app.config.from_object(config_by_name[test_config])

    # views 
    from .src.views import api_index, api_auth
    app.register_blueprint(api_index) #/ 메인화면
    app.register_blueprint(api_auth) #/auth 로그인 화면
    
    db.init_app(app)

    return app