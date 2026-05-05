from park import db
from datetime import datetime

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age_category = db.Column(db.String(20), nullable=False)  # adult/child
    tickets = db.relationship('Ticket', backref='visitor', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False)  # standard/vip/platinum
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime, nullable=False)
    remaining_time = db.Column(db.Integer)  # в минутах

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # extreme/adventure/classic
    min_age = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)