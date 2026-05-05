from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///park.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key'

    db.init_app(app)


    from park.views import main_bp
    app.register_blueprint(main_bp)

    return app