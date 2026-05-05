import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from park import create_app
from park.extensions import db
from park.common.models import Attraction, AccessRule, PriceList, User, Visitor

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if Attraction.query.first():
            print("⚠️ База уже заполнена")
            return

        print("🔄 Заполняю базу данных...")
        
        # Создаём тестового пользователя
        test_user = User(username='testuser', email='test@test.com', password='hashed_password')
        db.session.add(test_user)
        db.session.flush()  # Получаем ID
        
        # Создаём посетителя
        test_visitor = Visitor(user_id=test_user.id, name='Test User', phone='+1234567890', age_category='adult')
        db.session.add(test_visitor)
        
        # Аттракционы
        attractions = [
            Attraction(name='Карусель', category='classic', min_age=0, description='Классическая карусель', 
                      status='available', max_capacity=20, current_capacity=20),
            Attraction(name='Американские горки', category='extreme', min_age=14, description='Скоростные горки',
                      status='available', max_capacity=24, current_capacity=24),
            Attraction(name='Пиратский корабль', category='adventure', min_age=8, description='Качающийся корабль',
                      status='available', max_capacity=30, current_capacity=30),
        ]
        db.session.add_all(attractions)
        
        # Правила доступа
        rules = [
            AccessRule(ticket_status='standard', attraction_category='classic', allowed=True, priority_access=False),
            AccessRule(ticket_status='standard', attraction_category='extreme', allowed=False, priority_access=False),
            AccessRule(ticket_status='vip', attraction_category='extreme', allowed=True, priority_access=True),
            AccessRule(ticket_status='platinum', attraction_category='extreme', allowed=True, priority_access=True),
        ]
        db.session.add_all(rules)
        
        # Прайс-лист
        prices = [
            PriceList(ticket_status='standard', age_category='adult', price=500),
            PriceList(ticket_status='standard', age_category='child', price=300),
            PriceList(ticket_status='vip', age_category='adult', price=1000),
            PriceList(ticket_status='vip', age_category='child', price=700),
            PriceList(ticket_status='platinum', age_category='adult', price=1500),
            PriceList(ticket_status='platinum', age_category='child', price=1200),
        ]
        db.session.add_all(prices)
        
        db.session.commit()
        print("✅ База данных готова!")

if __name__ == '__main__':
    seed_database()