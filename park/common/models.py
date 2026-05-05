from ..extensions import db
from datetime import datetime

class Visitor(db.Model):
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Связь с логином
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    age_category = db.Column(db.String(20), nullable=False) # 'adult' или 'child'
    
    # Связи
    tickets = db.relationship('Ticket', backref='visitor', lazy=True)
    purchases = db.relationship('Purchase', backref='visitor', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'), nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False) # 'standard', 'vip', 'platinum'
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime, nullable=False)
    remaining_time = db.Column(db.Integer) # Остаток минут (для отслеживания времени)
    is_activated = db.Column(db.Boolean, default=False)
    
    # Связи
    visits = db.relationship('VisitRecord', backref='ticket', lazy=True)

class Attraction(db.Model):
    __tablename__ = 'attractions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False) # 'extreme', 'adventure', 'classic'
    min_age = db.Column(db.Integer, default=0) # Возрастное ограничение
    max_capacity = db.Column(db.Integer)
    
    # Связи
    visits = db.relationship('VisitRecord', backref='attraction', lazy=True)
    
class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    tickets = db.relationship('Ticket', backref='purchase', lazy=True)
    payments = db.relationship('Payment', backref='purchase', lazy=True)

class Payment(db.Model):
    """Таблица платежей"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='card') # card, cash
    status = db.Column(db.String(20), default='completed') # completed, pending
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

class VisitRecord(db.Model):
    __tablename__ = 'visit_records'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'), nullable=False)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, nullable=True)
    charged_time = db.Column(db.Boolean, default=True) # Списывалось ли время
    
    # Связи уже указаны выше в Ticket и Attraction

class AuditLog(db.Model):
    """Журнал действий (для отладки и безопасности)"""
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False) # create, update, delete, enter
    table_name = db.Column(db.String(50))
    record_id = db.Column(db.Integer)
    new_value = db.Column(db.Text) # JSON или строка с данными
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# --- Справочники (нужны для ЛР 4 и 5) ---

class AccessRule(db.Model):
    """Матрица доступа (Strategy)"""
    __tablename__ = 'access_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_status = db.Column(db.String(30), nullable=False) # standard, vip, platinum
    attraction_category = db.Column(db.String(50), nullable=False) # classic, adventure, extreme
    is_allowed = db.Column(db.Boolean, default=False)
    has_priority_access = db.Column(db.Boolean, default=False)

class PriceList(db.Model):
    """Прайс-лист билетов"""
    __tablename__ = 'price_list'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_status = db.Column(db.String(30), nullable=False)
    age_category = db.Column(db.String(20), nullable=False) # adult, child
    price = db.Column(db.Float, nullable=False)
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)