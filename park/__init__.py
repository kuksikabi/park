import os
from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(os.path.dirname(basedir), 'instance', 'park.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key'
    
    db.init_app(app)
    
    from park.common.models import User, Visitor, Attraction, Ticket, Purchase, Payment, AccessRule, PriceList, VisitRecord, AuditLog, Notification

    from park.views import main_bp
    app.register_blueprint(main_bp)
    
    return app