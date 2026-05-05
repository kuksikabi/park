from flask import Flask
from extensions import db
import os

def create_app():
    """Создать и настроить Flask приложение"""
    
    # Получаем путь к текущей директории
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Конфигурация
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///park.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key'
    
    # Инициализация базы данных
    db.init_app(app)
    
    # Регистрация blueprint
    from views import main_bp
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)