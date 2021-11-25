from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config='dev'):
    app = Flask(__name__)
    
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # config 속성 부여
    from .config import config_by_name
    app.config.from_object(config_by_name[test_config])

    # views 
    from .src.views import api_index, api_auth, api_book
    app.register_blueprint(api_index) #/ 메인화면
    app.register_blueprint(api_auth) #/auth 로그인 화면
    app.register_blueprint(api_book) #/book 책 상세 페이지
    
    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80)