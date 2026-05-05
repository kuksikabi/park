# seed_data.py - версия без импортов, работает всегда
import os
import sys

# Жёстко прописываем путь к проекту
PROJECT_ROOT = r"C:\Users\miste\OneDrive\Рабочий стол\park"
sys.path.insert(0, PROJECT_ROOT)

# Теперь импорты должны сработать
from park import create_app
from park.extensions import db
from park.common.models import Attraction, AccessRule, PriceList

def seed_database():
    print("🚀 Инициализация приложения...")
    app = create_app()
    
    with app.app_context():
        print("📦 Создаю таблицы БД...")
        db.create_all()
        
        if Attraction.query.first():
            print("⚠️ Данные уже есть, пропускаю заполнение.")
            return
        
        print("🔄 Заполняю тестовыми данными...")
        
        # Аттракционы
        db.session.add_all([
            Attraction(name='Карусель', category='classic', min_age=0, description='Классика', max_capacity=20),
            Attraction(name='Американские горки', category='extreme', min_age=14, description='Экстрим', max_capacity=24),
            Attraction(name='Пиратский корабль', category='adventure', min_age=8, description='Приключения', max_capacity=30),
        ])
        
        # Правила доступа
        db.session.add_all([
            AccessRule(ticket_status='standard', attraction_category='classic', is_allowed=True),
            AccessRule(ticket_status='standard', attraction_category='extreme', is_allowed=False),
            AccessRule(ticket_status='vip', attraction_category='extreme', is_allowed=True, has_priority_access=True),
            AccessRule(ticket_status='platinum', attraction_category='extreme', is_allowed=True, has_priority_access=True),
        ])
        
        # Цены
        db.session.add_all([
            PriceList(ticket_status='standard', age_category='adult', price=500),
            PriceList(ticket_status='vip', age_category='adult', price=1000),
            PriceList(ticket_status='platinum', age_category='adult', price=1500),
        ])
        
        db.session.commit()
        print("✅ База данных готова! Запускай runserver.py")

if __name__ == '__main__':
    seed_database()