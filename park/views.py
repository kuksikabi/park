# park/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from park.extensions import db  # <-- Добавь "park."
from park.common.models import Visitor, Attraction, Purchase, Payment, Ticket, VisitRecord, AuditLog
from park.common.services.ticket_service import TicketService
from park.common.services.access_control_service import AccessControlService
from datetime import datetime

main_bp = Blueprint('main', __name__)
ticket_service = None
access_service = None

def get_services():
    """Ленивая инициализация сервисов"""
    global ticket_service, access_service
    if ticket_service is None:
        ticket_service = TicketService(db.session)
    if access_service is None:
        access_service = AccessControlService()
    return ticket_service, access_service

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/attractions')
def attractions():
    """Список всех аттракционов"""
    all_attractions = Attraction.query.all()
    
    # Группировка по категориям
    categories = {
        'classic': [a for a in all_attractions if a.category == 'classic'],
        'adventure': [a for a in all_attractions if a.category == 'adventure'],
        'extreme': [a for a in all_attractions if a.category == 'extreme']
    }
    
    return render_template('attractions.html', categories=categories)

@main_bp.route('/attractions/<int:attraction_id>')
def attraction_details(attraction_id):
    """Детали аттракциона + форма прохода"""
    attraction = Attraction.query.get_or_404(attraction_id)
    
    # Если пользователь авторизован — показываем его билеты
    tickets = []
    if current_user.is_authenticated:
        visitor = Visitor.query.filter_by(user_id=current_user.id).first()
        if visitor:
            ts, _ = get_services()
            tickets = ts.get_tickets_by_visitor(visitor.id)
    
    return render_template('attraction_details.html', 
                         attraction=attraction, 
                         tickets=tickets)

@main_bp.route('/buy_ticket', methods=['GET', 'POST'])
@login_required
def buy_ticket():
    """Покупка нового билета"""
    ts, _ = get_services()
    visitor = Visitor.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type')
        
        try:
            # Расчёт цены
            price = ts.calculate_price(ticket_type, visitor.age_category)
            
            # Создаём покупку
            purchase = Purchase(
                visitor_id=visitor.id,
                total_amount=price
            )
            db.session.add(purchase)
            db.session.flush()
            
            # Создаём платёж (имитация)
            payment = Payment(
                purchase_id=purchase.id,
                payment_method='card',
                amount=price,
                status='completed'
            )
            db.session.add(payment)
            
            # Создаём билет
            duration = 240 if ticket_type == 'standard' else None  # 4 часа или бессрочный
            ticket_data = ts.create_ticket(
                visitor_id=visitor.id,
                purchase_id=purchase.id,
                ticket_status=ticket_type,
                age_category=visitor.age_category,
                duration_minutes=duration
            )
            
            db.session.commit()
            flash(f'🎫 Билет #{ticket_data["id"]} успешно куплен!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Ошибка: {str(e)}', 'danger')
    
    # GET — показываем форму
    return render_template('buy_ticket.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Личный кабинет: мои билеты"""
    visitor = Visitor.query.filter_by(user_id=current_user.id).first()
    ts, _ = get_services()
    tickets = ts.get_tickets_by_visitor(visitor.id) if visitor else []
    return render_template('dashboard.html', tickets=tickets)

@main_bp.route('/attractions/<int:attraction_id>/enter', methods=['POST'])
@login_required
def enter_attraction(attraction_id):
    """Проход через турникет"""
    ticket_id = request.form.get('ticket_id')
    if not ticket_id:
        flash('⚠️ Выберите билет', 'warning')
        return redirect(url_for('main.attraction_details', attraction_id=attraction_id))
    
    attraction = Attraction.query.get_or_404(attraction_id)
    ts, acs = get_services()
    
    # Получаем данные билета и посетителя
    ticket = Ticket.query.get_or_404(ticket_id)
    visitor = Visitor.query.get_or_404(ticket.visitor_id)
    
    # Проверяем доступ
    result = acs.validate_access(
        ticket_status=ticket.status,
        attraction_category=attraction.category,
        visitor_age=18 if visitor.age_category == 'adult' else 12,  # Упрощённо
        attraction_min_age=attraction.min_age,
        remaining_time=ticket.remaining_time
    )
    
    if result['allowed']:
        # Создаём запись о посещении
        visit = VisitRecord(
            ticket_id=ticket.id,
            attraction_id=attraction.id,
            entry_time=datetime.utcnow(),
            charged_time=True
        )
        db.session.add(visit)
        
        # Списываем время если нужно
        if ticket.remaining_time is not None:
            ticket.remaining_time = max(0, ticket.remaining_time - 15)  # -15 мин за посещение
        
        # Audit log
        audit = AuditLog(
            action='enter',
            table_name='visit_records',
            record_id=visit.id,
            new_value=f"attraction={attraction.name}, ticket={ticket.id}"
        )
        db.session.add(audit)
        db.session.commit()
        
        flash(f'✅ {result["message"]}', 'success')
    else:
        flash(f'🚫 {result["message"]}', 'error')
    
    return redirect(url_for('main.attraction_details', attraction_id=attraction_id))