from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config='dev'):
    # app = Flask(__name__, instance_relative_config=True)
    app = Flask(__name__)
    
    from .config import config_by_name
    app.config.from_object(config_by_name[test_config])

    from .src.views import api_auth, api_index
    app.register_blueprint(api_auth)
    app.register_blueprint(api_index)
    
    db.init_app(app)

    return app