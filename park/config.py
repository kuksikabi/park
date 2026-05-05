import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    # Самый надежный вариант для Windows: относительный путь от корня проекта
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/park.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False