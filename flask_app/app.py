from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        JSON_AS_ASCII = False  # 한글 깨짐 오류
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:devpass@127.0.0.1:3306/elice_flask_board"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.secret_key = 'asodfajsdofijac'
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app