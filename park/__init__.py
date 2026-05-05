import os
from flask import Flask
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    
    # Пути
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Поднимаемся на уровень выше папки park, чтобы найти instance
    root_dir = os.path.dirname(basedir)
    db_path = os.path.join(root_dir, 'instance', 'park.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key-123'
    
    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    with app.app_context():
        # Импортируем модели ЗДЕСЬ, чтобы избежать ImportError
        from park.common.models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        # Импорт и регистрация блюпринта
        from park.views import main_bp
        app.register_blueprint(main_bp)
    
    return app