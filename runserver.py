import os
from flask import Flask
from park.extensions import db  # ← Правильный импорт из подпакета

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/park.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key'
    
    db.init_app(app)
    
    from park.views import main_bp  
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)