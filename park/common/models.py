from ..extensions import db
from datetime import datetime
from flask_login import UserMixin

# ==================== USERS ====================
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Связи
    visitor = db.relationship('Visitor', backref='user', uselist=False, cascade="all, delete-orphan")


# ==================== VISITORS ====================
class Visitor(db.Model):
    __tablename__ = 'visitors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50))
    age_category = db.Column(db.String(20), nullable=False)  # adult/child
    
    # Связи
    tickets = db.relationship('Ticket', backref='visitor', lazy=True)
    purchases = db.relationship('Purchase', backref='visitor', lazy=True)


# ==================== ATTRACTIONS ====================
class Attraction(db.Model):
    __tablename__ = 'attractions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # classic/adventure/extreme
    status = db.Column(db.String(30))  # available/maintenance/closed
    min_age = db.Column(db.Integer, default=0)
    max_capacity = db.Column(db.Integer)
    current_capacity = db.Column(db.Integer)
    maintenance_notes = db.Column(db.Text)
    
    # Связи
    visits = db.relationship('VisitRecord', backref='attraction', lazy=True)


# ==================== VISIT RECORDS ====================
class VisitRecord(db.Model):
    __tablename__ = 'visit_records'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'), nullable=False)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, nullable=True)
    charged_time = db.Column(db.Boolean, default=True)
    
    # Связи уже указаны выше


# ==================== ACCESS RULES ====================
class AccessRule(db.Model):
    __tablename__ = 'access_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_status = db.Column(db.String(30), nullable=False)
    attraction_category = db.Column(db.String(50), nullable=False)
    allowed = db.Column(db.Boolean, default=False)
    priority_access = db.Column(db.Boolean, default=False)


# ==================== PRICE LIST ====================
class PriceList(db.Model):
    __tablename__ = 'price_list'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_status = db.Column(db.String(30), nullable=False)
    age_category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== PURCHASES ====================
class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30))  # pending/completed/cancelled
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    cashier_id = db.Column(db.Integer)
    
    # Связи
    tickets = db.relationship('Ticket', backref='purchase', lazy=True)
    payments = db.relationship('Payment', backref='purchase', lazy=True)


# ==================== PAYMENTS ====================
class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    payment_method = db.Column(db.String(30))  # card/cash/online
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Связи уже указаны выше


# ==================== TICKETS ====================
class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'), nullable=False)
    ticket_status = db.Column(db.String(30), nullable=False)
    age_category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Numeric(10, 2))
    valid_until = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    remaining_time = db.Column(db.Integer)
    
    # Связи
    visits = db.relationship('VisitRecord', backref='ticket', lazy=True)


# ==================== NOTIFICATIONS ====================
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Связи
    user = db.relationship('User', backref='notifications')


# ==================== AUDIT LOG ====================
class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)